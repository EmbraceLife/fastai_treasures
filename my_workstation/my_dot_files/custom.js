// leave at least 2 line with only a star on it below, or doc generation fails
/**
 *
 *
 * Placeholder for custom user javascript
 * mainly to be overridden in profile/static/custom/custom.js
 * This will always be an empty file in IPython
 *
 * User could add any javascript in the `profile/static/custom/custom.js` file.
 * It will be executed by the ipython notebook at load time.
 *
 * Same thing with `profile/static/custom/custom.css` to inject custom css into the notebook.
 *
 *
 * The object available at load time depend on the version of IPython in use.
 * there is no guaranties of API stability.
 *
 * The example below explain the principle, and might not be valid.
 *
 * Instances are created after the loading of this file and might need to be accessed using events:
 *     define([
 *        'base/js/namespace',
 *        'base/js/events'
 *     ], function(IPython, events) {
 *         events.on("app_initialized.NotebookApp", function () {
 *             IPython.keyboard_manager....
 *         });
 *     });
 *
 * __Example 1:__
 *
 * Create a custom button in toolbar that execute `%qtconsole` in kernel
 * and hence open a qtconsole attached to the same kernel as the current notebook
 *
 *    define([
 *        'base/js/namespace',
 *        'base/js/events'
 *    ], function(IPython, events) {
 *        events.on('app_initialized.NotebookApp', function(){
 *            IPython.toolbar.add_buttons_group([
 *                {
 *                    'label'   : 'run qtconsole',
 *                    'icon'    : 'icon-terminal', // select your icon from http://fortawesome.github.io/Font-Awesome/icons
 *                    'callback': function () {
 *                        IPython.notebook.kernel.execute('%qtconsole')
 *                    }
 *                }
 *                // add more button here if needed.
 *                ]);
 *        });
 *    });
 *
 * __Example 2:__
 *
 * At the completion of the dashboard loading, load an unofficial javascript extension
 * that is installed in profile/static/custom/
 *
 *    define([
 *        'base/js/events'
 *    ], function(events) {
 *        events.on('app_initialized.DashboardApp', function(){
 *            require(['custom/unofficial_extension.js'])
 *        });
 *    });
 *
 * __Example 3:__
 *
 *  Use `jQuery.getScript(url [, success(script, textStatus, jqXHR)] );`
 *  to load custom script into the notebook.
 *
 *    // to load the metadata ui extension example.
 *    $.getScript('/static/notebook/js/celltoolbarpresets/example.js');
 *    // or
 *    // to load the metadata ui extension to control slideshow mode / reveal js for nbconvert
 *    $.getScript('/static/notebook/js/celltoolbarpresets/slideshow.js');
 *
 *
 * @module IPython
 * @namespace IPython
 * @class customjs
 * @static
 */



// Go to Running cell shortcut
Jupyter.keyboard_manager.command_shortcuts.add_shortcut('Alt-I', {
                                                        help : 'Go to Running cell',
                                                        help_index : 'zz',
                                                        handler : function (event) {
                                                        setTimeout(function() {
                                                                   // Find running cell and click the first one
                                                                   if ($('.running').length > 0) {
                                                                   //alert("found running cell");
                                                                   $('.running')[0].scrollIntoView();
                                                                   }}, 250);
                                                        return false;
                                                        }
                                                        });


// create my details droplist
Jupyter.keyboard_manager.edit_shortcuts.add_shortcut('Ctrl-Shift-M', {
                              help : 'add details drop',
                              help_index : 'zz',
                              handler : function (event) {
                              var target = Jupyter.notebook.get_selected_cell()
                              var cursor = target.code_mirror.getCursor()
                              var before = target.get_pre_cursor()
                              var after = target.get_post_cursor()
                              target.set_text(before + '[/details][details=""]' + after)
                              cursor.ch += 20 // where to put your cursor
                              target.code_mirror.setCursor(cursor)
                              return false;
                              }}
                                                        );






// create my multiline snippet
require(["nbextensions/snippets_menu/main"], function (snippets_menu) {
        console.log('Loading `snippets_menu` customizations from `custom.js`');
        var horizontal_line = '---';
        var my_favorites = {
        'name' : 'My favorites',
        'sub-menu' : [
                      {
                      'name' : 'most_jupyter_magics',
                      'snippet' : ['%reload_ext autoreload',
                                   '%autoreload 2',
                                   '%matplotlib inline',
                                   'from IPython.core.interactiveshell import InteractiveShell',
                                   'InteractiveShell.ast_node_interactivity = "all"',],
                      },
                      {
                      'name' : 'kaggle download links',
                      'snippet' : ['from IPython.display import FileLinks',
                                   'FileLinks(\'.\')',],
                      },
                      {
                      'name' : 'details_drop',
                      'snippet' : ['[/details][details=""]',],
                      },
                      {
                      'name' : 'find snippet custom js',
                      'snippet' : ['echo $(jupyter --config-dir)/custom/custom.js',],
                      },
                      ],
        };
        snippets_menu.options['menus'].push(snippets_menu.default_menus[0]);
        snippets_menu.options['menus'][0]['sub-menu'].push(horizontal_line);
        snippets_menu.options['menus'][0]['sub-menu'].push(my_favorites);
        console.log('Loaded `snippets_menu` customizations from `custom.js`');
        });
