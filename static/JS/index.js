function cli(v) {
    $(document).ready(function () {
        $.post("ad", {
                v: v.toString()
            },
            function (data, status) {
                if (status == "success") {
                    var win = window.open(data, '_blank');
                    if (win) {
                        win.focus();
                    } else {
                        alert('Please allow popups for this website');
                    }
                }
            });

    });
}