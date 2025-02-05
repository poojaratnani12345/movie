frappe.pages['first'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'user_page',
		single_column: true
	});
}