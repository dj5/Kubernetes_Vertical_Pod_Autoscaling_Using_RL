# Kubernetes_Vertical_Pod_Autoscaling_Using_RL
<h1>Installing kubectl using curl</h1>

<p>This set of instructions will guide you on how to install 
<code>kubectl</code> on a Linux machine using <code>curl</code>.</p>

<h2>Prerequisites</h2>
<ul>
  <li>A Linux machine with root access.</li>
  <li><code>curl</code> and <code>sudo</code> packages installed.</li>
</ul>

<h2>Step 1: Download kubectl</h2>
<p>Run the following command to download the latest stable version of 
<code>kubectl</code>:</p>

<pre><code>curl -LO "https://dl.k8s.io/release/$(curl -L -s 
https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"</code></pre>

<h2>Step 2: Install kubectl</h2>
<p>Run the following command to install <code>kubectl</code>:</p>

<pre><code>sudo install -o root -g root -m 0755 kubectl 
/usr/local/bin/kubectl</code></pre>

<p>This will install <code>kubectl</code> to 
<code>/usr/local/bin/kubectl</code> and set the necessary permissions.</p>

<h2>Verify kubectl installation</h2>
<p>To verify that <code>kubectl</code> is installed and working properly, 
run the following command:</p>

<pre><code>kubectl version --client</code></pre>

<p>This should display the client version of <code>kubectl</code> you just 
installed.</p>


