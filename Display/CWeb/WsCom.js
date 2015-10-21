$(document).ready(function(){
            $('form#register').submit(function(event) {
                $.ajax( {
                    type:'Get',
                    url:'http://' + location.host + '/subscribe/cab',
                    success:function(data) {
                        $('#lbl_id').text(data['id_cab'].toString());
                        $('#lbl_channel').text(data['channel'].toString());
                    }
                })
                return false;
            });
            $('form#simulation').submit(function(event) {
                $.ajax( {
                    type:'Get',
                    url:'http://' + location.host + '/simulation/start_move',
                    success:function(data) {
                    }
                })
                return false;
            });
            var socket;
            $('form#connect').submit(function(event) {
            // Connection
                socket = new WebSocket("ws://" + location.host + "/cab_device");
                socket.onopen = function() {
                    message = {'id_cab': $('#lbl_id').text() };
                    socket.send(JSON.stringify(message));
                };
                socket.onclose = function() {
                   $('#log').append('Socket closed <br/>');
                };
                socket.onmessage = function(evt){
                    $('#log').append(evt.data + '<br/>');
                    cab = eval("(" + evt.data.replace("False","false").replace("True", "true") + ')')
                    $('#lbl_isbusy').text(cab['is_busy'].toString());
                    $('#lbl_odometer').text(cab['odometer'].toString());
                }
                return false;
            });
            // Envoi message
			$('form#send').submit(function(event) {
                socket.send($('#send_data').val());
                return false;
            });
            // Deconnection
			$('form#disconnect').submit(function(event) {
                socket.close();
                return false;
            });
        });