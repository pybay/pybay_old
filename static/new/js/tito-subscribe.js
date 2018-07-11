jQuery.fn.shake = function(amount){
  $(this).velocity('callout.shake')
}

jQuery(function(){
  $('#register-interest-form').submit(function(e){
    var name  = $('#tito-register-name').val()
    var email = $('#tito-register-email').val()
    if($.trim(name) != '' && $.trim(email) != '')
    {
      var url = ["https://ti.to/sf-python/pybay2018/interested_users/subscribe.json?&interested_user[email]=", email , "&interested_user[name]=", name, "&callback=?"].join('')
      $.getJSON(url, null, function(data){})
      $('#register-interest-form h2').fadeIn();
    }
    e.preventDefault();
    return false;
  })
})
