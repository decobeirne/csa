% rebase('base.tpl')

<form method="post" action="login">
    <input type="hidden" name="next" value="{{next}}">
    <p>username <input type="text" name="username"></p>
    <p>password <input type="password" name="password"></p>
    <p><input type="submit" value="Submit"></p>
</form>