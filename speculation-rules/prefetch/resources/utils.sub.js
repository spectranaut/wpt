/**
 * Utilities for initiating prefetch via speculation rules.
 */

// Resolved URL to find this script.
const SR_PREFETCH_UTILS_URL = new URL(document.currentScript.src, document.baseURI);

class PrefetchAgent extends RemoteContext {
  constructor(uuid, t, https) {
    super(uuid);
    this.t = t;
    this.https = https;
  }

  getExecutorURL(options = {}) {
    let {cross_origin_host, https, ...extra} = options;
    let params = new URLSearchParams({uuid: this.context_id, ...extra});
    let base = new URL(SR_PREFETCH_UTILS_URL);
    if(https==null) {
        https = this.https;
    }
    if(cross_origin_host) {
      base.hostname = "{{hosts[alt][www.www1]}}";
    }
    base.protocol = https ? "https://" : "http://";
    base.port = https ? "{{ports[https][0]}}" : "{{ports[http][0]}}";
    return new URL(`executor.sub.html?${params}`, base.href);
  }

  // Requests prefetch via speculation rules.
  //
  // In the future, this should also use browser hooks to force the prefetch to
  // occur despite heuristic matching, etc., and await the completion of the
  // prefetch.
  async forceSinglePrefetch(url, extra = {}) {
    await this.execute_script((url, extra) => {
      insertSpeculationRules({ prefetch: [{source: 'list', urls: [url], ...extra}] });
    }, [url, extra]);
    return new Promise(resolve => this.t.step_timeout(resolve, 3000));
  }

  async navigate(url) {
    await this.execute_script((url) => {
      window.executor.suspend(() => {
        location.href = url;
      });
    }, [url]);
    assert_equals(
        await this.execute_script(() => location.href),
        url.toString(),
        "expected navigation to reach destination URL");
    await this.execute_script(() => {});
  }

  async getRequestHeaders() {
    return this.execute_script(() => requestHeaders);
  }
}

// Must also include /common/utils.js and /common/dispatcher/dispatcher.js to use this.
async function spawnWindow(t, https = true) {
  let agent = new PrefetchAgent(token(), t, https);
  let w = window.open(agent.getExecutorURL());
  t.add_cleanup(() => w.close());
  return agent;
}

function insertSpeculationRules(body) {
  let script = document.createElement('script');
  script.type = 'speculationrules';
  script.textContent = JSON.stringify(body);
  document.head.appendChild(script);
}

async function prefetch_test(t, https_src_url, https_prefetch_url, extra_rules = {}) {
  assert_implements(HTMLScriptElement.supports('speculationrules'), "Speculation Rules not supported");

  let agent = await spawnWindow(t, https_src_url);
  let nextUrl = agent.getExecutorURL({ https: https_prefetch_url, page: 2 });
  await agent.forceSinglePrefetch(nextUrl, extra_rules);
  await agent.navigate(nextUrl);
  return await agent.getRequestHeaders();
}
function excpect_prefetch_success(requestHeaders) {
  assert_in_array(requestHeaders.purpose, ["", "prefetch"], "The vendor-specific header Purpose, if present, must be 'prefetch'.");
  assert_equals(requestHeaders.sec_purpose, "prefetch");
}

function excpect_prefetch_failure(requestHeaders) {
  assert_equals(requestHeaders.purpose, "", "Prefetch should not work with HTTP scheme.");
  assert_equals(requestHeaders.sec_purpose, "", "Prefetch should not work with HTTP scheme.");
}
