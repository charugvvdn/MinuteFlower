function create_give(time_start, time_end, repeat, charity_id) {
    $.post('/api/give/create/', {
        csrfmiddlewaretoken:getCookie('csrftoken'),
        time_start:time_start,
        time_end:time_end,
        repeat:repeat,
        charity:charity_id
    }, function(res) {
        console.log(res);
    });
}

function delete_give(give_id) {
    $.post('/api/give/delete/', {
        csrfmiddlewaretoken:getCookie('csrftoken'),
        give:give_id
    }, function(res) {
        console.log(res);
    });
}

function list_gives() {
    $.get('/api/give/', function(res) {
        console.log(res);
    });
}

function show_give(give_id) {
    $.get('/api/give/{0}/'.format(give_id), function(res) {
        console.log(res);
    });
}

function login(username, password) {
    $.post('/api/login/', {
        csrfmiddlewaretoken:getCookie('csrftoken'),
        username:username,
        password:password
    }, function(res) {
        console.log(res);
    });
}

function logout() {
    $.get('/api/logout/', function(res) {
        console.log(res);
    });
}
