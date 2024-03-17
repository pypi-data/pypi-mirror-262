<h1>JustSimplestDB</h1>
<h2>Author</h2>
<p>Jakub Aleksander Michalski</p>
<p>Email: <a href="mailto:jakub.michalski.aleksander@gmail.com">jakub.michalski.aleksander@gmail.com</a></p>

<h2>Description</h2>
<p>JustSimplestDB is a Python library designed to simplify database management. It aims to provide a user-friendly interface for interactingwith databases, potentially reducing the complexity associated with traditional DBMS (Database Management Systems).</p>

<h2>Features</h2>
<ul>
    <li>Version 1.1, Update date: 13.03.2024.<br>
    Description:<br>
    Added separator attribute to Instance class,
    which allows you to use custom separators for reading data from .txt file.<br>
    Default value is TAB(<code>justsimplestdb.Instance("example", separator="\t"</code>)</li>
    <li>Patch note:<br>
    Version 1.1.1, Update date: 16.03.2024.<br>
    Description:<br>
    Fixed DBMS Shell, when you used other separators than TAB, Shell was rising a WrongSeparator exception.</li>
    <li>Ease of use: Designed to be easy to learn and use, making it accessible for users with varying levels of programming experience.</li>
</ul>

<h2>Considerations</h2>
<ul>
    <li>Security: It's important to note that currently the database file is not encrypted.<br>
    Consider implementing encryption for sensitive data storage in future versions.</li>
</ul>

<h2>Additional Information</h2>
<p>Full Documentation: <a href="https://github.com/M1ch5lsk1/JustSimplestDB/tree/main">https://github.com/M1ch5lsk1/JustSimplestDB/tree/main</a></p>
