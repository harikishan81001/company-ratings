$(document).ready(function() {
    function draw(data) {
        canvas = '<canvas id="canvas" width="600" height="400"></canvas>'
        $("#exampleModal .modal-body").html(canvas)
        var canvas = $('#canvas');
        var ctx = canvas[0].getContext("2d");
        var data_points = []
        $.each(data.labels, function(i, val){
            data_points.push(data.data[val])
        })

        var chart = new Chart(ctx).Line({
            labels: data.labels,
            datasets: [
                {
                    fillColor: "rgba(190,144,212,0.2)",
                    strokeColor: "rgba(190,144,212,1)",
                    pointColor: "rgba(190,144,212,1)",
                    pointStrokeColor: "#fff",
                    pointHighlightFill: "#fff",
                    pointHighlightStroke: "rgba(220,220,220,1)",
                    data: data_points
                },
            ]
        }, {});
    }

    $("#selectError").on("change", function(){
        $.ajax({
            url: '/company/matrix/',
            method: 'GET',
            data: {company: $(this).val()},
            success: function(data){
                $("#exampleModal").modal("show")
                draw(data)
            }
        })
    });
    $("#exampleModal").on("hidden.bs.modal", function(){
        $('#canvas').remove()
    })
})
