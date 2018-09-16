% rebase('base.tpl')

<script>
$(function () {
    addEntry = function (elm, type) {
        var parent = elm.parentNode;  // E.g. <div class="input-container">
        var newContainer = $('<div class="input-container"></div>');
        if (type == 'admin') {
            newContainer.append('<input type="text" name="' + type + '$new" value="">');
        }
        else if (type == 'editor') {
            newContainer.append('<input type="text" name="' + type + '$new" value="">');
            // TODO: add drop down with permissions for farms or "None"
        }
        else if (type == 'farm') {
            newContainer.append('<input type="text" name="' + type + '$new" value="">');
        }
        newContainer.append('<div class="edit-farm-align-right"><span class="edit-farm-control" onclick="deleteEntry(this)">Delete</span></div>');
        newContainer.insertBefore(parent);
    };
});

$(function () {
    deleteEntry = function (elm, type) {
        var inputContainer = $(elm).parent().parent();  // E.g. <div class="input-container"><div class="edit-farm-align-right">
        inputContainer.remove();
    };
});
</script>

<form method="post" enctype="multipart/form-data" action="{{root_rel_dir}}admin">

    <p class="edit-farm-instruction">
        <i class="fa fa-info-circle"></i> Add, remove or update values and click <b>Update database</b> at the bottom of the page to save to the server, or <b>Cancel</b> to undo your changes and refresh this page.
        <br>
        <i class="fa fa-info-circle"></i> Any admin or editor added is given the default password "csa", which they should reset asap.
    </p>

    <div class="edit-farm-container">
        <p class="edit-farm-key">Admins</p>
        % for admin in permissions_dict['admins']:
            <div class="input-container">
                <input type="text" name="admin$existing" value="{{admin}}" style="background-color:#e3ede9" readonly>
                <div class="edit-farm-align-right">
                    <span class="edit-farm-control" onclick="deleteEntry(this)">Delete</span>
                </div>
            </div>
        % end
        <p>
            <span class="edit-farm-control" onclick="addEntry(this, 'admin')">Add admin</span>
        </p>
    </div>

    <div class="edit-farm-container">
        <p class="edit-farm-key">Editors</p>
        % for editor in permissions_dict['editors']:
            <div class="input-container">
                <input type="text" name="editor$existing" value="{{editor}}" style="background-color:#e3ede9" readonly>
                <div class="edit-farm-align-right">
                    <span class="edit-farm-control" onclick="deleteEntry(this)">Delete</span>
                </div>
            </div>
        % end
        <p>
            <span class="edit-farm-control" onclick="addEntry(this, 'editor')">Add editor</span>
        </p>
    </div>

    <div class="edit-farm-container">
        <p class="edit-farm-key">Farms</p>
        <p class="edit-farm-instruction">
            <i class="fa fa-info-circle"></i> If adding a new farm, it should be given a simple, unique ID, i.e. lowercase with no punctuation or spaces. This is not displayed on the website, only used internally.
            <br>
            <i class="fa fa-info-circle"></i> Note that ID is not the title, which should be a human-readable string, and can be set on the <b>edit</b> page.
            <br>
            <i class="fa fa-info-circle"></i> WARNING: deleting a farm will delete all content from the server.
        </p>
        % for farm in permissions_dict['farms']:
            <div class="input-container">
                <input type="text" name="farm$existing" value="{{farm}}" style="background-color:#e3ede9" readonly>
                <div class="edit-farm-align-right">
                    <span class="edit-farm-control" onclick="deleteEntry(this)">Delete</span>
                </div>
                <div class="edit-farm-align-right">
                    <span class="edit-farm-control" onclick="window.location.href = '{{root_rel_dir}}edit/{{farm}}'">Edit farm profile</span>
                </div>
            </div>
        % end
        <p>
            <span class="edit-farm-control" onclick="addEntry(this, 'farm')">Add farm</span>
        </p>
    </div>

    <div class="input-container">
        <input class="edit-farm-submit" type="submit" value="Update database">
        <span class="edit-farm-control" onclick="window.location.href = '{{root_rel_dir}}admin'">Cancel</span>
    </div>
</form>
