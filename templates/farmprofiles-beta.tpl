% rebase('base.tpl')

<script>
var setup = function() {
    setupLinks();
};
window.onload = setup;
</script>


<form method="post" action="farmprofiles-beta">
    Name: <input type="text" name="name">
    <input type="submit" value="Submit">
</form>


