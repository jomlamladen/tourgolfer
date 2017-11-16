 var map;
    var center;
    var marker;
    var markers = [];
    var global_lat,global_lng;
    $(function() {

        var navigation              =  $('.nav-link-li');
        var allcontents             = $('.site-content');
        var input                   = $("#search-autocomplete");
        var inputbtn                = $("#search-btn");
        var postStatus              = $('#post-btn');
        var userbox                 = $('.user');
        var chat_item               = $('.chat-item');
        var chat_list               = $('#chatlister');
        var chat_box                = $('#chatbox');
        var chat_back               = $('.back-msg-btn');
        var tournament_modal        = $('#tournaments-modal');
        var tournament_modal_open   = '.tournament-open-modal';
        var tournament_list         = $('.tournament-list');
        var user_box                = $('.users-list > .user')
        var tournament_modal_name   = $('.tournament-modal-name');
        var login_page              = 'index.html';
        var user_list               = $('.users-list');
        var status_data             = $('#post-data');
        var tournament_content_list = $('#tournament-content .tournament-list');
        var req_login               = '';
        var req_logout              = '';
        var req_logout              = 'user/logout';
        var req_tournament          = 'tournaments/'
        var req_all_tournaments     = 'tournaments';
        var req_timeline            = 'timeline';
        var req_user_login          = 'user/login';
        var center                  =  new google.maps.LatLng(59.76522, 18.35002);

        navigation.on('click',function () {
            allcontents.hide();
           $('#'+ $(this).attr('data-url')).show();
             if($(this).attr('data-url') === "users-content"){
                 get_all_users()
             }
              if($(this).attr('data-url') === "timeline-content"){
                  get_timeline()
              }
              if($(window).width() < 820)
              {
                  $('.navbar-toggle').trigger('click')
              }
        });

        inputbtn.on('click',function () {
            user_box.css('display','none');
            user_box.each(function (i,item) {
                console.log(item);
                if($(this).attr('data-first_name').toLowerCase().search(input.val().toLowerCase()) !== -1){

                    $(this).css('display','block')
                }
            })

        });

        chat_item.on('click',function () {
            chat_list.hide();
            chat_box.show(100);

        });
        chat_back.on('click',function () {
            chat_box.hide();
            chat_list.show(100);
        })
        
        tournament_list.on('click','.tournament_modal_open',function () {
                    var center = new google.maps.LatLng(parseFloat($(this).attr('data-lat')), parseFloat($(this).attr('data-lng')));

           
                    tournament_modal.modal({
                        backdrop: 'static',
                        keyboard: false
                    }).on('shown.bs.modal', function () {
                                                   RemoveAllMarkers();

                           var marker = new google.maps.Marker({
                                map: map,
                                position: center
                            });
                           markers.push(marker)
                        google.maps.event.trigger(map, 'resize');
                        map.setCenter(center);
                        map.setZoom(16);
                        // map.clear();

                        markers.setMap(map);

                    });
            // tournament_modal.modal('show', function () {
                    // var ltng= {lat: parseFloat($(this).attr('data-lat')),lng: parseFloat($(this).attr('data-lng'))};

                    //  // var latlng = new google.maps.LatLng($(this).attr('data-lat'), $(this).attr('data-lng'));
                    // var map_id = window[jQuery('#tournament_location').attr('id')];
                    // google.maps.event.trigger(map_id, 'resize'); 
                    // map_id.setCenter(ltng);
                    // marker.setMap(map_id);

                    // var center = new google.maps.LatLng(59.76522, 18.35002);
            // });
        })
   
        var global_url = 'http://tourgolfer.digitalcube.rs:8802/api/';
        var global_url_user = 'http://tourgolfer.digitalcube.rs:8802/';
        var shoot = function(url, data, method, on_success, on_error, token) {
            var _headers = {};
            if (token) {
                _headers.authorization = token;
            }
            var _settings =  {
                url: url,
                data: data,
                method: method,
                dataType: 'json',
                headers: _headers
            };
            console.log('SETTINGS', _settings);
            $.ajax(_settings).done( function(res) {
                reset_info();
                if (on_success && typeof on_success === 'function') {
                    on_success(res);
                }
            }).fail( function(res) {
                if (on_error && typeof on_error === 'function') {
                    on_error(res);
                }
            });
        }
        var reset_info = function() {
        }
        var call_error = function(res) {
            // console.log('ERROR', res);
            $('#info').html(res.responseJSON['message']);
            $('#info').addClass('error');
        }
        var logout_ok = function(res)  {
            // console.log('SUCCESS LOGIN', res);
            localStorage.clear()
            window.location.href = login_page;
        }
        var logout = function() {
            var _userdata = '';
            var _url = global_url_user + req_logout;
            var _token = localStorage.getItem('token');
            // console.log('log', _userdata, _url, _token);
            shoot(_url, _userdata, 'POST', logout_ok, call_error, _token);
        }
        var join_tournament = function(tournament_id) {
            var _userdata = {
                "following_only": false
            };
            var _url = global_url + req_tournament +tournament_id;
            var _token = localStorage.getItem('token');
            // console.log('log', _userdata, _url, _token);
            shoot(_url, _userdata, 'PUT', join_tournament_ok, call_error, _token);
        }
        var join_tournament_ok = function (res) {
            $('.tour-'+res.id_tournament).addClass('follow-active');
            $('.tour-'+res.id_tournament).addClass('unjoin-user-btn');
            $('.tour-'+res.id_tournament).removeClass('join-user-btn');
            $('.tour-'+res.id_tournament+' .dd').html('joined');
            var html ='<div style="display: inline-block" class="'+res.id_tournament+'-'+res.image+'" ><img style="display:inline-block; margin-left:10px; margin-top:5px;border-raidus:50%; width: 30px; height:30px; overflow: hidden; border:1px solid white; -webkit-border-radius: 50%;-moz-border-radius: 50%;border-radius: 50%; background-size: cover; " width="30" height="30" src="img/users/'+res.image+'.jpg"></div>'
           $('.joined-'+res.id_tournament+'').prepend(html);
        }
        var unjoin_tournament = function(tournament_id) {
            var _userdata = {};
            var _url = global_url + req_tournament + tournament_id;
            var _token = localStorage.getItem('token');
            // console.log('log', _userdata, _url, _token);
            shoot(_url, _userdata, 'DELETE', unjoin_tournament_ok, call_error, _token);
        }
        var unjoin_tournament_ok = function (res) {
            $('.tour-'+res.id_tournament).removeClass('follow-active');
            $('.tour-'+res.id_tournament).addClass('join-user-btn');
            $('.tour-'+res.id_tournament).removeClass('unjoin-user-btn');
            $('.tour-'+res.id_tournament+' .dd').html('join');
            $('.'+res.id_tournament+'-'+$('.userprofileimgx').attr('data-img-name')).remove();
            // console.log('unjoin ',res)
        }
        var get_tournaments = function() {
            var _userdata = '';
            var _url = global_url + req_all_tournaments;
            var _token = localStorage.getItem('token');
            console.log('log', _userdata, _url, _token);
            shoot(_url, _userdata, 'GET', get_tournaments_ok, call_error, _token);
        }
        var get_all_users = function() {
            var _userdata = {
            };
            var _url = global_url + 'users';
            var _token = localStorage.getItem('token');
            // console.log('log', _userdata, _url, _token);
            shoot(_url, _userdata, 'GET', get_all_users_ok, call_error, _token);
        }
        var get_all_users_ok = function (res) {
            // console.log(res);
              //            $('.joined-'+res.id_tournament+'').prepend(html);
            var html= '<div class="row">';
                $(res.users).each(function (i,item) {
                    var image = item['image'];
                          //                    if(image===false){image = "user.png";}else{
                          //                        image = image+'.jpg';
                          //                    }
                    if(i % 4 == 0){
                        html +='</div><div class="row">';
                    }
                    html +='<div class="col-sm-3 col-md-3 user  animated fadeInUp" data-first_name="'+item['first_name'] +' ' +item['last_name']+'">'+
                        '<div class="user-item">'+
                        '<div class="" style="margin:auto;padding-left:20%;">' +
                        '<div style="margin:auto;width:100px;height:100px; background:url(img/users/'+image+'.jpg) no-repeat;background-size:cover;  margin:0;margin-top:5px;border-raidus:50%;  overflow: hidden; border:1px solid white; -webkit-border-radius: 50%;-moz-border-radius: 50%;border-radius: 50%; border:1px solid green;"/></div>'+
                        ''+
                        '<div class="usertag">'+item['first_name'] +' ' +item['last_name']+'</div>'+
                        '<div class="social-buttons">'+
                        '<div class="follow-button"><i class="glyphicon glyphicon-user"></i></div>'+
                        '<div class="follow-button"><i class="glyphicon glyphicon-share"></i></div>'+
                        '<div class="follow-button"><i class="glyphicon glyphicon-envelope"></i></div>'+
                        '</div>'+
                        '</div>'+
                        '</div>';
                })
                html+='</div>';

               user_list.html(html);
        }

        var get_timeline = function() {
            var _userdata = {
            };
            var _url = global_url + req_timeline;
            var _token = localStorage.getItem('token');
            // console.log('log', _userdata, _url, _token);
            shoot(_url, _userdata, 'GET', get_timeline_ok, call_error, _token);
        }
        var get_timeline_ok = function (res) {
            // console.log(res);
            var html = '';
            $(res.timeline).each(function (i, item) {
                if (item['user'] !== null) {
                    console.log(item['user']['image'])
                    console.log("PPPERA",item['text']);
                    
                    html += '<div class="box box-widget timecard animated fadeInUp" style="margin-top:10px">' +
                        '<div class="box-header with-border">' +
                        '<div class="user-block">' +
                        '<img class="img-circle" width="30" src="img/users/' + item['user']['image'] + '.jpg" alt="User Image">' +
                        '<span class="user-profile-img" style="padding-left:5px;">' + item['user']['first_name'] + ' ' + item['user']['last_name'] + '</span>' +
                        '<span class="posted-time push-right">' + moment(item['time']).format('MM/DD/YYYY  HH:mm') + '</span>' +

                        '</div>' +
                        '<p>' + item['text'].replace(/</g, "&lt;").replace(/>/g, "&gt;") + '</p>' +
                        '</div>' +
                        '<div class="timecard-box-body text-box">' +

                        '<div class="col-xs-12  col-sm-8 col-sm-push-1 col-md-8 col-md-offset-1 info-box" style="">' +

                        '<div class="col-sm-12 social-box">' +
                        '<div class="social-buttons">' +

                        ' <div class="follow-button"><i class="glyphicon glyphicon-user"></i></div>' +
                        '<div class="follow-button"><i class="glyphicon glyphicon-share"></i></div>' +
                        '<div class="follow-button"><i class="glyphicon glyphicon-envelope"></i></div>' +
                        '</div>' +
                        '</div>' +
                        '</div>' +
                        '</div>' +

                        '</div><hr>';

                }else{
                    html += '<div class="box box-widget timecard animated fadeInUp" style="margin-top:10px">' +
                        '<div class="box-header with-border">' +
                        '<div class="user-block">' +
                        '<span class="posted-time push-right">' + moment(item['time']).format('MM/DD/YYYY HH:mm') + '</span>' +

                        '</div>' +
                        '<p>' + item['text'] + '</p>' +
                        '</div>' +
                        '<div class="timecard-box-body text-box">' +

                        '<div class="col-xs-12  col-sm-8 col-sm-push-1 col-md-8 col-md-offset-1 info-box" style="">' +

                        '<div class="col-sm-12 social-box">' +
                        '<div class="social-buttons">' +

                        ' <div class="follow-button"><i class="glyphicon glyphicon-user"></i></div>' +
                        '<div class="follow-button"><i class="glyphicon glyphicon-share"></i></div>' +
                        '<div class="follow-button"><i class="glyphicon glyphicon-envelope"></i></div>' +
                        '</div>' +
                        '</div>' +
                        '</div>' +
                        '</div>' +

                        '</div><hr>';
                }
            })
                $('.timeline-box').html(html);

            // console.log('join ',res)
        }


        var get_tournaments_ok = function (res) {
            // console.log('SUCCESS', res);
            var html = '';

            $(res.tournaments).each(function (i, item) {
                var day = moment(item['date_start']).format('D')
                var month = moment(item['date_start']).format('MMM')
                var year = moment(item['date_start']).format('YYYY')
                var dDay = moment(item['date_start']);
                var current = moment();
                var dif_day = dDay.diff(current, 'days')   // =1
                var diff_days = moment(item['date_start']).format('YYYY')
                var status = 'joined';
                var data_status ='unjoin-user-btn';
                var active = 'follow-active';
                if(item['status'] === "non_following"){ active = ''; status='join'; data_status = 'join-user-btn';}

                html += '<li>'+
                    '<time datetime="2014-07-20">'+
                    '    <span class="day">'+ day +'</span>'+
                    '    <span class="month">'+ month +'</span>'+
                    '    <span class="year"></span>'+
                    '    <span class="time">'+ dif_day +'</span>'+
                    '</time>'+
                    '<div class="info">'+
                    '    <h2 class="title"><a  style="text-decoration:none;color:green;" href="'+ item['website']+'" target="_blank">'+ item['name'] +'</a></h2>'+
                      //                    '<p class="desc">United States Holiday</p>'+
                    '<div class="bg-logo" style=""></div>'+

                    '<div class="tournament-buttons">'+

                    '<div class="follow-button '+active+' tour-'+item['id']+' '+data_status+'" data-join_id="'+item['id'] +'"><i class="glyphicon glyphicon-user"></i>'+
                        '<span class="dd">'+status+'</span>' +
                    '</div>'+
                    '<div class="follow-button "><i class="glyphicon glyphicon-share"></i>' +
                    '<span class="dd">share</span></div>'+
                    '<div class="follow-button tournament_modal_open" data-name="'+item['name']+'" data-lat="'+item['coordinates']['lat']+'" data-lng="'+item['coordinates']['lon']+'"><i class="glyphicon glyphicon-map-marker"></i>' +
                    '<span class="dd">location</span></div>'+

                    '</div>'+
                    '</div>'+
                    '<div class="joined-users joined-'+item['id']+' ">';
                          var sarr = item['participants'];


                            if(sarr.length > 0){

                                $(sarr).each(function (e, etim) {
                                  // console.log(etim);

                                    html +='<div class="'+item.id+'-'+etim+'" style="display: inline-block" ><img style="display:inline-block; margin-left:10px; margin-top:5px;border-raidus:50%; width: 30px; height:30px; overflow: hidden; border:1px solid white; -webkit-border-radius: 50%;-moz-border-radius: 50%;border-radius: 50%; background-size: cover; " width="30" height="30" src="img/users/'+etim+'.jpg"></div>'
                                })
                              }
                    html+='</div>'+
                    '</li>';
            })
            tournament_content_list.html(html);
        }
        var check_token = function (_token) {
            if (_token !== null && _token !== undefined) {
                var _url = global_url_user+req_user_login;
                var _userdata = '';
                shoot(_url, _userdata, 'GET', get_check_token_ok, get_check_token_error, _token);
            }else{
                window.location.href = login_page;
            }
        }
        postStatus.on('click',function(){
                var _token = localStorage.getItem('token');
                var _url = global_url+'status';
                var _userdata = {
                  "status" : status_data.val()
                };
                shoot(_url, _userdata, 'PUT', post_status_ok, post_status_error, _token);
        })
        var post_status_ok = function(res) {
            console.log('SUCCESS GET OPTION', res);

        }
         
        var post_status_error = function(res) {
            console.log('SUCCESS GET OPTION', res);
        }
        var get_check_token_ok = function(res) {
            console.log('SUCCESS GET OPTION', res);
                $('body').css('display','block');
                var name=res['first_name'] + ' ' + res['last_name']
            $('.userprofileimgx').attr('src','img/users/'+res['picture']+'.jpg')
            $('.usertagx').html(name);
            $('.userprofileimgx').attr('data-img-name',res.picture);
            $('.userfollowers').html(res['followers']);
            $('.userfollowing').html(res['following']);

        }
        var get_check_token_error = function(res) {
            console.log(res);
            window.location.href = login_page;
        }


        $(document).ready(function() {

            check_token(localStorage.getItem('token'));
            get_tournaments();
            $('.logout').on('click', logout);
            var that = this;
            tournament_list.on('click','.join-user-btn',function (e) {
                join_tournament($(e.currentTarget).attr('data-join_id'))
            } );
            tournament_list.on('click','.unjoin-user-btn',function (e) {
                unjoin_tournament($(e.currentTarget).attr('data-join_id'))
            } );


        });
    })
    function setAllMap(map) {
          for (var i = 0; i < markers.length; i++) {
            markers[i].setMap(map);
          }
        }
    function RemoveAllMarkers() {
        while (markers.length > 0) {
            markers.pop().setMap(null);
        }
        markers.length = 0;
    }
    function initMap() {

        var mapOptions = {
            zoom: 7,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            center: center
        };

        map = new google.maps.Map(document.getElementById('tournament_location'), mapOptions);

        // var marker = new google.maps.Marker({
        //     map: map,
        //     position: center
        // });
    }
      // function initMap() {
      //      center = {lat: 22, lng: 22};
      //      map = new google.maps.Map(document.getElementById('tournament_location'), {
      //         zoom: 4,
      //         center: center
      //     });
      //     marker = new google.maps.Marker({
      //         position: center,
      //         map: map
      //     });

      // }
      // initialize();

