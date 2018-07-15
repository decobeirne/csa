% rebase('base.tpl')

<script>
var setup = function() {
    setupLinks();
};
window.onload = setup;
</script>

<p>Login</p>




<form method="post" action="login">
    <p>username <input type="text" name="username"</p>
    <p>password <input type="text" name="password"</p>
    <p><input type="submit" value="Submit"></p>
</form>

