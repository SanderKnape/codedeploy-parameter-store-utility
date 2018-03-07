<?php

$config = require './config.php';

echo "<h1>CodeDeploy secrets</h1>
<p>We can log in to the database with the username <strong>${config['user']}</strong> and the very secret password <strong>${config['password']}</strong></p>";
