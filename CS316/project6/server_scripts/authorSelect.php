<?php
$servername = "localhost";
$username = "user";
$password = "password";
$dbname = "dbname";

echo "
<!DOCTYPE html>

<html lang=\"en\">
    <head>
        <meta charset=\"utf-8\" />
        <meta name=\"viewport\" content=\"width=device-width\"/>
        <title>Ben Richey</title>
        <link rel=\"stylesheet\" href=\"../styles/constants.css\"/>
        <script src=\"http://code.jquery.com/jquery-3.1.0.min.js\"></script>
    </head>
    <body>
        <header>
            <h1>Ben Richey</h1>
            <div class=\"headerContent\">
                <form id=\"theme\">
                    <button id=\"themeBttn\">Light Mode</button>
                </form>
                <figure id=\"profilePic\">
                    <img id=\"headshot\" src=\"../images/headshot.PNG\" alt=\"A picture of myself\" title=\"Ben Richey Headshot\"
                    />
                    <figcaption>
                        <cite>Photo by <a href=\"https://www.morgansnellingsphotography.com\">
                                Morgan Snellings</a>. Instagram:
                            <a href=\"https://www.instagram.com/morgansnellingsphotography\">
                            @morgansnellingsphotography</a></cite>
                    </figcaption>
                </figure>
            </div>
        </header>
        <main>
            <nav>
                <a href=\"/pages/ben-richey.html\"><strong>Home</strong></a>
                <a href=\"/pages/resume.html\"><strong>My Resume</strong></a>
                <a href=\"/pages/myWork.html\"><strong>My Work</strong></a>
                <a href=\"/pages/myInterests.html\"><strong>My Interests</strong></a>
                <a href=\"/pages/theOfficeQuote.php\"><strong>The Office Quote of the Day</strong></a>
                <a href=\"/pages/report.html\"><strong>Report Bugs or Feature Requests</strong></a>
            </nav>
            <section class=\"content\">
                <h2 class=\"contentHeader\">The Office Quote Generator</h2>
                <p class=\"about\">The Office is my favorite TV show! Here's a random quote that is
                                   one of my favorites.</p>
            <figure>
		<p id='quote'></p>
		<figcaption></figcaption>
	    </figure>
	    <form method=\"post\" action=\"http://localhost/server_scripts/authorSelect.php\">
                        <legend>Want a random quote from a specific character?</legend>
                        <p>Type their name here to see if we have one or hit randomize to go back to random quotes.</p></br>
                        <label>The Office Character</label>
                        <input type=\"text\" name=\"character\" placeholder=\"ex: Michael Scott\"/>
			<input type=\"submit\" name=\"submitBttn\"/>
			<button name=\"random\">Randomize</button>

            </form>
            </section>
            <section class=\"contact\">
                <h2 class=\"contentHeader\">Contact</h2>
                <ul>
                    <li><p>
                        Email: <a href=\"mailto:bbri226@g.uky.edu\">bbri226@g.uky.edu</a>
                        </p>
                    </li>
                    <li><p>
                            <a href=\"https://www.linkedin.com/in/ben-richey-0b967a18a\">LinkedIn
                            </a>
                        </p>
                    </li>
                </ul>
            </section>
        </main>
    </body>
    <script type=\"text/javascript\" src=\"../scripts/theme.js\"></script>
</html>
";
if (isset($_POST["submitBttn"])) {
	// Data received. Collect it and query DB for quote from author
	$author = $_POST["character"];
	if (strlen($author) > 100) {
		echo("<script type=\"text/javascript\">alert('Error: Character name is too long.');</script>");
	} else {
		$conn = new mysqli($servername, $username, $password, $dbname);
		if ($conn->connect_error) {
		die("<script> type=\"text/javascript\"alert(\"Connection to server database failed.\");</script>");
		}
		$sql = "SELECT speaker, quote, season, episode FROM theOfficeQuotes WHERE speaker = '" . $author . "' ORDER BY RAND() LIMIT 1;";
		$result = $conn->query($sql);
		if ($result->num_rows > 0) {
			$row = $result->fetch_assoc();
                        echo "<script type=text/javascript>
                                var abt = document.querySelector(\".about\");
                                abt.innerHTML = \"Success! Found a quote by " . $author . ".\";
                                var quote = document.querySelector(\"#quote\");
                                quote.innerHTML = \"" . $row["quote"] . "\";
                                var caption = document.querySelector(\"#quote + figcaption\");
				caption.innerHTML = \"-" . $row["speaker"] . ", The Office, Season " . $row["season"] . ", Episode " . $row["episode"] . "\";
				</script>";
		} else {
                        echo "<script type=text/javascript>
                                var abt = document.querySelector(\".about\");
				abt.innerHTML = \"Uh oh! We don't have any quote's from " . $author . " just yet.\";
			      </script>";
		}
		$conn->close();
	}
} else if (isset($_POST["random"])) {
		$conn = new mysqli($servername, $username, $password, $dbname);
		if ($conn->connect_error) {
		die("<script> type=\"text/javascript\"alert(\"Connection to server database failed.\");</script>");
		}
		$sql = "SELECT speaker, quote, season, episode FROM theOfficeQuotes ORDER BY RAND() LIMIT 1;";
		$result = $conn->query($sql);
		if ($result->num_rows > 0) {
			$row = $result->fetch_assoc();
                        echo "<script type=text/javascript>
                                var abt = document.querySelector(\".about\");
                                abt.innerHTML = \"The Office is my favorite TV show! Here's a random quote that is one of my favorites.\";
                                var quote = document.querySelector(\"#quote\");
                                quote.innerHTML = \"" . $row["quote"] . "\";
                                var caption = document.querySelector(\"#quote + figcaption\");
				caption.innerHTML = \"-" . $row["speaker"] . ", The Office, Season " . $row["season"] . ", Episode " . $row["episode"] . "\";
				</script>";
		} else {
                        echo "<script type=text/javascript>
                                var abt = document.querySelector(\".about\");
				abt.innerHTML = \"Uh oh! It appears an error occured. Please report this on the report bugs and features page.\";
			      </script>";
		}
		$conn->close();
}
?>
