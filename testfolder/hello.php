<?php
	class Student {
		public $name;
		public function __construct($name){
			$this->name = $name;
		}
		public function getName() {
			return $this->name . "\n";
		}
	
		public function newStudent(){
			return "Student's name is " . $this->name . "\n";
		}
	}

	$test = new Student('Zain Quraishi');
	echo $test->newStudent();
	echo $test->getName();
?>
