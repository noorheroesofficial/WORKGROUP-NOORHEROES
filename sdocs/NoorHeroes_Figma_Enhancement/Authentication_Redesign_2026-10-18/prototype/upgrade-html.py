from pathlib import Path
p=Path(__file__).with_name('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('href="style.css"','href="style.css"><link rel="stylesheet" href="auth-v2.css"')
s=s.replace('<button data-view="language">Language</button>','<button data-view="registration">Registration</button><button data-view="language">Language</button>')
a=s.index('<select id="scenario"')
b=s.index('</select>',a)+9
s=s[:a]+'''<select id="scenario" aria-label="Controlled mock HTTP scenario"><option value="success">HTTP 200 · Success</option><option value="422">HTTP 422 · Field error</option><option value="422-global">HTTP 422 · General error</option><option value="500">HTTP 500 · Server failure</option><option value="503">HTTP 503 · Unavailable</option><option value="429">HTTP 429 · Rate limit (3 seconds)</option><option value="401">HTTP 401 · Authentication failure</option><option value="403">HTTP 403 · Request rejected</option><option value="network">Network failure</option><option value="timeout">Timeout (3 seconds)</option></select>'''+s[b:]
s=s.replace('</aside>','<p id="review-result" role="status">Fictional review data only. Requests use the local mock server.</p></aside>',1)
s=s.replace(' aria-disabled="true"','',1)
s=s.replace('<div class="brand"><img src="logo.png" alt="NoorHeroes"></div>','<img class="toolbar-wordmark" src="logo.png" alt="NoorHeroes"><div class="brand"><img src="monogram.png" alt=""></div>')
s=s.replace('<p id="validation"','<p id="validation"')
s=s.replace('<div id="status" role="status" hidden></div>','')
needle='<div class="submit-space">'
consent='''<div class="consent" hidden><div class="consent-line"><input id="consent-check" type="checkbox" aria-label="Review required consents"><span>I accept <button id="terms-open" type="button">Terms and Conditions</button> and <button id="privacy-open" type="button">Privacy Policy</button></span></div></div><button class="optional" type="button"><span>Optional preferences</span><span aria-hidden="true">›</span></button>'''
s=s.replace(needle,consent+needle,1)
s=s.replace('<span>Continue with Google</span>','<span class="button-label">Continue with Google</span><span class="dots" aria-hidden="true"><i></i><i></i><i></i></span>',1)
s=s.replace('<footer><button aria-disabled="true">Register</button><button aria-disabled="true">Forgot access</button></footer>','<footer><span id="account-copy"></span> <button id="account-link" class="footer-link"></button></footer>')
s=s.replace('<script src="countries.js"></script><script src="app.js"></script>', '''<div id="snackbar" role="alert" hidden><span id="snack-text"></span><button id="retry">Retry</button><button id="snack-close" aria-label="Dismiss notification">×</button></div>
<dialog id="legal-dialog" aria-labelledby="legal-title"><div class="sheet"><div class="handle"></div><div class="sheet-heading"><h2 id="legal-title"></h2><button id="legal-close" class="icon-button" aria-label="Close document">×</button></div><div id="legal-content"></div><button id="legal-agree" class="primary"></button></div></dialog>
<script src="countries.js"></script><script src="vendor/libphonenumber-max.js"></script><script src="vendor/validator.min.js"></script><script src="auth-core.cjs"></script><script src="app-v2.js"></script>''')
p.write_text(s,encoding='utf-8')
