<?php
$servername = "localhost";
$username = "user";
$password = "password";
$dbname = "dbname";
$tableName = "userReports";

function checkInput() {
	$badinput = FALSE;
	if (strlen($_POST["name"]) > 100) {
		echo("<script type=\"text/javascript\">alert(\"Error: Name must be < 100 characters\");</script>");
		$badinput = TRUE;
	}
	if (strlen($_POST["phoneNumber"]) > 20) {
		echo("<script> type=\"text/javascript\"alert(\"Error: phone number too long\");</script>");
		$badinput = TRUE;
	}
	if (strlen($_POST["email"]) > 50) {
		echo("<script> type=\"text/javascript\"alert(\"Error: email too long\");</script>");
		$badinput = TRUE;
	}
	if (strlen($_POST["state"]) > 50) {
		echo("<script> type=\"text/javascript\"alert(\"Error: state too long\");</script>");
		$badinput = TRUE;
	}
	if (strlen($_POST["county"]) > 100) {
		echo("<script> type=\"text/javascript\"alert(\"Error: county too long\");</script>");
		$badinput = TRUE;
	}
	if (strlen($_POST["requestType"]) > 30) {
		echo("<script> type=\"text/javascript\"alert(\"Error: request type too long\");</script>");
		$badinput = TRUE;
	}
	if (strlen($_POST["request"]) > 1000) {
		echo("<script> type=\"text/javascript\"alert(\"Error: request message too long\");</script>");
		$badinput = TRUE;
	}
	if (((INT)$_POST["aestheticAppeal"] > 6) or ((INT)$_POST["aestheticAppeal"] < 0)) {
		echo("<script> type=\"text/javascript\"alert(\"Error: Invalid rating for website aesthetic.\");</script>");
		$badinput = TRUE;
	}
	if (((INT)$_POST["logic"] > 6) or ((INT)$_POST["logic"] < 0)) {
		echo("<script> type=\"text/javascript\"alert(\"Error: Invalid rating for website ease of use.\");</script>");
		$badinput = TRUE;
	}
	return $badinput;
}

readfile("/var/www/benrdotcom/pages/report.html");
if (isset($_POST["submitBttn"])) {
	// Data received. Collect it and store in database
	$name = $_POST["name"];
	$number = $_POST["phoneNumber"];
	$email = $_POST["email"];
	$state = $_POST["state"];
	$county = $_POST["county"];
	$reqType = $_POST["requestType"];
	$report = $_POST["request"];
	$aesthetic = $_POST["aestheticAppeal"];
	$ease = $_POST["logic"];
	// Check input sizes
	$badinput = checkInput();
	// Connect to database
	if ($badinput === FALSE) {
		$conn = new mysqli($servername, $username, $password, $dbname);
		if ($conn->connect_error) {
		echo("<script> type=\"text/javascript\"alert(\"Connection to server database failed.\");</script>");
		}
		$sql = "INSERT INTO userReports (name, phoneNumber, email, state, county, requestType, request, aesthetic, logic)
			VALUES ('" . $name . "', '" . $number . "', '" . $email . "', '" . $state . "', '" . $county . "', '" . $reqType . "', '" . $report . "', " . $aesthetic . ", " . $ease .");";
		if ($conn->query($sql) === TRUE) {
		echo("<script type=\"text/javascript\">alert(\"Report submitted.\");</script>");
		} else {
		echo("<script type=\"text/javascript\">alert(\"Error: Unable to submit report: " . $conn->error . "\");</script>");
		}
	}
}
?>
