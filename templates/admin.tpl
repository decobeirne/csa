% rebase('base.tpl')

<div class="admin-container">
    <h3>Admins</h3>
    % for admin in admins:
        <p>{{admin}}: DELETE, RESET PASSWORD</p>
    % end
    <p>Add admin</p>
    
    <h3>Editors</h3>
    % for editor in editors.keys():
        <p>{{editor}}, farm={{editors[editor]}}: DELETE, RESET PASSWORD, SET FARM PERMISSION</p>
    % end
    <p>Add editor</p>
    
    <h3>Farms</h3>
    % for farm in farms:
        <p>{{farm}}: DELETE</p>
    % end
    <p>Add farm</p>
</div>

