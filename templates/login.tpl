% rebase('base.tpl')

<form method="post" action="login">
    <p>Enter usename and password to sign in. Contact admin if any difficulties.</p>
    <input type="hidden" name="next" value="{{next}}">
    <p>username <input type="text" name="username"></p>
    <p>password <input type="password" name="password"></p>
    <div class="input-container">
        <input type="submit" value="Submit">
    </div>
</form>