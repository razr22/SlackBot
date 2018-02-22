--TEST--
boo() function - A basic test to see if it works. :)
--FILE--
<?php
include 'hello.php'; // might need to adjust path if not in the same dir
$far = 'Hello World';
var_dump(boo($far));
?>
--EXPECT--
string(11) "Hello World"
