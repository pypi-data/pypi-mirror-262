$(document).ready(function () {
    var url_string = window.location.href;
    var url = new URL(url_string);
    var tab = url.searchParams.get("tab");
    if (tab !== null) {
        $('#tab-' + tab).click();
    }

    $(window).on('detailmap:ready', function (e, data) {
        // Get some current object properties
        var verbosename = $('body').attr('data-app-verbosename');
        var objectsname = $('body').attr('data-objectsname');
        var modelname = $('body').attr('data-modelname');

        var layername = `${modelname}_layer`;
        var url = window.SETTINGS.urls[layername];
        var loaded_layer = false;
        var map = data.map;

        var style = L.Util.extend({ clickable: false },
            window.SETTINGS.map.styles[modelname] || {});

        var layer = new L.ObjectsLayer(null, {
            modelname: modelname,
            style: style,
            // Filter to not display current detail object on layer 
            filter: function filterWithoutCurentPk(el)  {
                if (el.properties.id === parseInt($('body').attr('data-pk'))) {
                    return false;
                }
                return true;
            },
        });
        map.layerscontrol.addOverlay(layer, objectsname, verbosename);

        // Change the group layer "verbosename" (current object list) in first position
        var allOverlaysLayers = document.getElementsByClassName('leaflet-control-layers-overlays')[0];
        allOverlaysLayers.insertBefore(allOverlaysLayers.lastChild, allOverlaysLayers.firstChild);

        // Add object family layer (without current object) 
        map.on('layeradd', function (e) {
            var options = e.layer.options || { 'modelname': 'None' };
            if (!loaded_layer && options.modelname === modelname && options.modelname !== data.modelname) {
                layer.load(url);
                map.addLayer(layer);
                loaded_layer = true;
            }
        });

        // Remove object family layer (without current object) 
        map.on('layerremove', function (e) {
            var options = e.layer.options || { 'modelname': 'None' };
            if (loaded_layer && options.modelname === modelname && options.modelname !== data.modelname) {
                map.removeLayer(layer);
                loaded_layer = false;
            }
        });
    });
});