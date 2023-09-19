function getParameterByName(name) {
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)');
    var results = regex.exec(window.location.href);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

var monParametre = getParameterByName('web_proxy_requested_website');

if (monParametre !== null) {
    document.cookie = 'web_proxy_requested_website=' + monParametre + '; path=/;';
    console.log('Cookie créé avec succès : mon_parametre=' + monParametre);
} else {
    console.log('Le paramètre "mon_parametre" n\'existe pas dans l\'URL.');
}