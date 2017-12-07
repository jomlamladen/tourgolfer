
var tabs_btn            = $('.tabs-click')
        var login_form          = $("#login-form")
        var register_form       = $("#register-form");
        var register_active     = $('.register');
        var login_active        = $('.login');
        var info_msg            = $('#info');
        var region_active       = $('.region');
        var profile_page        =' profile.html';
        var form_email = $('#email');
        var form_reg_pass = $('#reg_password');
        var form_first_name = $('#first_name');
        var form_last_name = $('#last_name');
        var req_user_register   = 'user/register';
        var req_user_login      = 'user/login'
        var form_login_username = $('#login_username');
        var form_login_password = $('#login_password');
    $(function() {

    
        tabs_btn.click(function(e) {
    		if($(this).attr('id') == 'login-tab'){
                login_form.delay(100).fadeIn(100);
                register_form.fadeOut(100);
                register_active.removeClass('active');
                $(this).addClass('active');
    		}else{
                register_form.delay(100).fadeIn(100);
                login_form.fadeOut(100);
                login_active.removeClass('active');
                $(this).addClass('active');
    		}

        });



        var global_url = 'http://tourgolfer.digitalcube.rs:8802/api/';
        var global_url_user = 'http://tourgolfer.digitalcube.rs:8802/';

        var set_regions = function () {
            var _url = global_url+'regions';

            shoot(_url, '', 'GET', region_ok, call_error);

        }
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

        var call_error = function(res) {
            // console.log('ERROR', res);
            $('#info').html(res.responseJSON['message']);
            $('#info').addClass('error');
        }

        var reset_info = function() {
            info_msg.html('');
            info_msg.removeClass('error');
            info_msg.removeClass('success');
        }

        var register_ok = function(res) {
            // console.log('SUCCESS REGISER', res);
            info_msg.html('Thank you for registration <br> You will be redirected.');
            //        setTimeout(function () {
            // console.log(res.token);
            if(res.token !== undefined){
                set_token(res.token);
            }
             setTimeout(function(){  location.href = profile_page;},1500);
            

            // set_token(res.token);
            //        },2000);
        }


        var region_ok = function(res) {
            // console.log('SUCCESS REGION GET', res);
            $(res.regions).each(function (i,item) {
                region_active.append('<option value="'+item['id']+'">'+item['name_ger']+'</option>')
            });
        }
        
        var register = function() {
            var _userdata = {
                "username": form_email.val(),
                "password": form_reg_pass.val(),
                "data" : {
                   "first_name" : form_first_name.val(),
                   "last_name" : form_last_name.val()
                }
            }
            var _userdata = JSON.stringify(_userdata);
            var _url = global_url_user+ req_user_register;
            console.log('Log', _userdata, _url);
            shoot(_url, _userdata, 'POST', register_ok, call_error);
        }

        var login_ok = function(res)  {
            // console.log('SUCCESS LOGIN', res);
            info_msg.html('Succesfully loged in. You will be redirect in few seconds. ')
            set_token(res.token);
                //        setTimeout(function () {
              location.href = profile_page;

            //        },2000)
        }

        var login = function() {
            var _userdata = {
                "username" : form_login_username.val(),
                "password" : form_login_password.val()
            };
            var _url = global_url_user+req_user_login;
            console.log('log', _userdata, _url);
            shoot(_url, _userdata, 'POST', login_ok, call_error);
        }

        var set_token = function (token) {
            localStorage.clear();
            localStorage.setItem("token", token);
        }

        var check_token = function (_token) {
            if (_token !== null && _token !== undefined) {
                var _url = global_url_user+req_user_login;
                var _userdata = '';
                shoot(_url, _userdata, 'GET', get_check_token_ok, get_check_token_error, _token);
            }
        }

        var get_check_token_ok = function(res) {
            // console.log('SUCCESS GET OPTION', res);
            if(res) {
                location.href = profile_page;
            }
        }
        var get_check_token_error = function(res) {

        }




    $(document).ready(function() {

            check_token(localStorage.getItem('token'));
            set_regions();
            $('#register-submit').on('click', register);
            $('#login-submit').on('click', login);
            $('#logout').on('click', logout);

        }
    );
});

