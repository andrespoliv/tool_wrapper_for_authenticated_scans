<h1>Tool wrapper for authenticated scans</h1>

<p>Commands are specifically made for Powershell and tools are uploaded in .exe format, in case of running from Linux adjust commands.py file and use binary files accordingly.</p>

<h2>Support</h2>
<li><a href="https://github.com/projectdiscovery/nuclei">Nuclei</a></li>
<li><a href="https://github.com/projectdiscovery/katana">Katana</a></li>
<li><a href="https://github.com/bitquark/shortscan">Shortscan</a></li>

<h2>Installation</h2>
<p>Install dependencies</p>
<code>pip install -r requirements.txt</code>

<h2>Usage</h2>
<p>Basic example</p>
<code>python main.py -u {username} -p {password} -t {toolname} --authurl https://example-login-page.com</code>
<br></br>
<p>Set specific scan URL example</p>
<code>python main.py -u {username} -p {password} -t {toolname} --authurl https://example-login-page.com --scanurl https://target.com</code>
<br></br>
<p>Add parameters specific to the used tool example</p>
<code>python main.py -u {username} -p {password} -t {toolname} --authurl https://example-login-page.com -a "--verbose --random-agent"</code>

<h2>Disclaimer</h2>
<p>I don't own any of the tools supported. This tool is meant for Bug Bounty hunters, Pentesters and Security Professionals, don't apply it to applications you're not allowed to.</p>

<h2>Acknowledgements</h2>
<strong>Special thanks to Project Discovery and bitquark.</strong>