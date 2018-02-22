<?php
declare(strict_types=1);

include_once("hello.php");

	class Output extends \PHPUnit_Framework_TestCase {
		public function testString(){
			$this->student = new Student('Zain Quraishi');
			$this->assertEquals($this->student->newStudent(), 'Student\'s name is Zain Quraishi' . "\n");
		}
	}
?>
