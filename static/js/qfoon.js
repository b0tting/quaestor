/**
 * Created by Mark on 22-2-2017.
 */
var table = ""

      function get_my_time() {
          date = new Date();
          return date.getHours() + ":" + ( (date.getMinutes()<10?'0':'') + date.getMinutes() )
      }

      function refresh_jira() {
          table.ajax.reload();

        $.getJSON( "jiratotal", function( data ) {
                total = data["total"];
                $("#jiraunassigned").text(total + " unassigned!");
                label = $("#jiraunassigned_label");
                label.removeClass("bg-red bg-green bg-yellow");
                if(total > 20) {
                    label.addClass("bg-red")
                } else if(total >10) {
                    label.addClass("bg-yellow")
                } else {
                    label.addClass("bg-green")
                }

                if ( total == 0) {
                      $('#jira_table').hide();
                      $('#jira_happy').show()
                } else {
                      $('#jira_happy').hide();
                      $('#jira_table').show()
                  }

            });
          $("#jiradate").text(get_my_time());
      }

    function refresh_phones() {
        $.getJSON( "phones", function( data ) {
            try {
                for (target in data) {
                    id_target = "#" + target.replace(" ", "_");
                    if (data[target] && $(id_target).length) {
                        $(id_target).html(data[target].replace("(", "<br>("));
                        if (data[target] != "None") {
                            $(id_target + "_label").removeClass("bg-red");
                            $(id_target + "_label").addClass("bg-green")
                        } else {
                            $(id_target + "_label").addClass("bg-red");
                            $(id_target + "_label").removeClass("bg-green")
                        }
                    }

                }
            } catch(err) {
                console.log("Got an error trying to get phone info" + err)
            }
            $("#phonedate").text(get_my_time())
        }).fail(function() {console.log("Got tough love from the server trying to get phone info")})
    }

    function startTime() {
        var today = new Date();
        var h = today.getHours();
        var m = today.getMinutes();
        if (m < 10) {
            m = "0" + m
        }
        $('#clock').text(h + ":" + m)
        setTimeout(startTime, 500);
    }

      $( document ).ready(function() {
            startTime();
            table = $('#jira_table').DataTable({
                "sAjaxSource": "/jira",
                "fnServerData": function ( sSource, aoData, fnCallback, oSettings ) {
                  oSettings.jqXHR = $.ajax( {
                    "dataType": 'json',
                    "type": "GET",
                    "url": sSource,
                    "data": aoData,
                    "success": fnCallback,
                      "timeout": 5000
                  } )},
                 "aaSorting": [],
                "paging":   false,
                "ordering": false,
                "info":     false,
                "searching": false,
                "columnDefs": [
                        {className: "icon-columns", "targets": [0,1]},
            {

                // The `data` parameter refers to the data for the cell (defined by the
                // `data` option, which defaults to the column being worked with, in
                // this case `data: 0`.
                "render": function ( data, type, row ) {
                    return '<img src="/jira_image/' + row[0].replace("https://jira.qualogy.com/", "")+ '" style="width: 32px; height: 32px;">'
                },
                "targets":0
            }, {
                "render": function ( data, type, row ) {
                    return '<img src="/jira_image/' + row[1].replace("https://jira.qualogy.com/", "")+ '" style="width: 32px; height: 32px;">';
                },
                "targets":1
            }, {
                "render": function ( data, type, row ) {
                    val = row[3]
                    if (row[6]) {
                        val = '<i class="fa fa-fw fa-tag" style="color: red"></i><b>' + row[3] + '</b>';
                    }

                    if (row[7]) {
                        val = " <small style='color: grey'>" + row[7] + "</small>  | " + val
                    }
                    return val

                },
                "targets":3
            },
                                    {
                "targets": [ 6,7 ],
                "visible": false
            }

                    ]
        });
          refresh_jira();
          refresh_phones();
          setInterval(refresh_phones, 600000);
          setInterval(refresh_jira, 300000)
      });



