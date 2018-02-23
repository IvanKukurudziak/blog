function detailShow() {
    var reader = new FileReader()
    var new_html = reader.read('../templates/blog/post_detail.html');
    alert(new_html);

}
