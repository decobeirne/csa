% rebase('base.tpl')

<script>
var setup = function() {
    setupLinks();
};
window.onload = setup;
</script>


<p>
admin
<br>
{{data}}
<br>
user is {{user}}

</p>

<p>
<a href="logout">logout</a>
</p>
