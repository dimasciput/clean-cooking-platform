let addedLayers = [];
let rasterBoundaryLayer = null;
const loadingSpinner1 = document.getElementById('loading-spinner-1');
const loadingSpinner0 = document.getElementById('loading-spinner-0');

MAPBOX = new mapboxgl.Map({
    container: 'map', // container ID
    style: mapboxStyle,
    center: [0, 0], // starting position [lng, lat]
    zoom: 2, // starting zoom
    preserveDrawingBuffer: true
});
MAPBOX.first_symbol = 'poi_label';

const fetchRasterBoundary = async () => {
    await fetch(rasterBoundary).then(response => response.arrayBuffer()).then(
        data => {
            rasterBoundaryLayer = data
        }
    )
}

fetch(geojsonBoundary).then(response => response.json()).then(
    async data => {
        MAPBOX.on('load', async () => {
            MAPBOX.addSource('boundary', {
                type: 'geojson',
                data: data
            });
            MAPBOX.addLayer({
                'id': 'boundary-layer',
                'type': 'line',
                'source': 'boundary',
                'paint': {
                    'line-width': 2,
                    'line-color': 'red'
                }
            });
            bbox = turf.extent(data);
            const l = bbox[0];
            const r = bbox[2];
            const d = bbox[1];
            const u = bbox[3];
            coords = [[l, u], [r, u], [r, d], [l, d]];
            MAPBOX.coords = coords;
            MAPBOX.fitBounds(bbox, {padding: 20});
            BBOX = bbox;
            await fetchRasterBoundary();
        });
    }
)

const clipSelectedLayerPromise = (boundary, layerId, drawToMap = true) => {
    return new Promise((resolve, reject) => {
        const url = '/api/clip-layer-by-region/';
        fetch(url, {
            method: 'POST',
            credentials: "same-origin",
            headers: {
                'X-CSRFToken': csrfToken,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                boundary: boundary,
                layer_id: layerId
            })
        }).then((response) => response.json()).then(async data => {
            if (data['status'] === 'Pending') {
                setTimeout(async () => {
                    resolve(clipSelectedLayer(boundary, layerId, drawToMap));
                }, 1000)
            } else if (data['status'] === 'Success') {
                resolve("FINISH")
            } else {
                reject('Error clipping layer')
            }
        }).catch((error) => reject(error))
    })
}

const clipSelectedLayer = async (boundary, layerId, drawToMap = true) => {
    const url = '/api/clip-layer-by-region/';
    await fetch(url, {
        method: 'POST',
        credentials: "same-origin",
        headers: {
            'X-CSRFToken': csrfToken,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            boundary: boundary,
            layer_id: layerId
        })
    }).then((response) => response.json()).then(async data => {
        if (data['status'] === 'Pending') {
            setTimeout(async () => {
                await clipSelectedLayer(boundary, layerId, drawToMap);
            }, 1000)
        }
        else if (data['status'] === 'Success') {
            const output = data.output;
            console.log("FINISH")
        } else {
            console.error('Error clipping layer')
        }
    }).catch((error) => console.log(error))
}

(function () {
    const scenarioSelect = document.getElementById('scenarioSelect');
    const ccaToolBtn = document.getElementById('cca-tool-btn');
    const ccaReportBtn = document.getElementById('report-btn');
    let selectedScenario = null;
    let selectedLayers = null;

    scenarioSelect.onchange = async (e) => {
        // Clear canvas
        let eaiCanvas = document.getElementById('eai-output');
        eaiCanvas.getContext('2d').clearRect(0, 0, eaiCanvas.width, eaiCanvas.height);

        let aniCanvas = document.getElementById('ani-output');
        aniCanvas.getContext('2d').clearRect(0, 0, aniCanvas.width, aniCanvas.height);

        let demandCanvas = document.getElementById('demand-output');
        demandCanvas.getContext('2d').clearRect(0, 0, demandCanvas.width, demandCanvas.height);

        let supplyCanvas = document.getElementById('supply-output');
        supplyCanvas.getContext('2d').clearRect(0, 0, supplyCanvas.width, supplyCanvas.height);

        ccaToolBtn.disabled = true;
        loadingSpinner1.style.display = "block";
        loadingSpinner0.style.display = "block";
        selectedScenario = e.target.options[e.target.selectedIndex];
        selectedLayers = JSON.parse(selectedScenario.dataset.layers);
        let datasetUrl = selectedScenario.dataset.url;
        let inputString = new URL(datasetUrl).searchParams.get('inputs')
        let inputs = inputString.split(',')

        if (addedLayers.length > 0) {
            for (let i = 0; i < addedLayers.length; i++) {
                const addedLayer = addedLayers[i];
                MAPBOX.removeLayer(addedLayer);
                MAPBOX.removeSource(addedLayer);
            }
            addedLayers = [];
        }
        if (selectedLayers.length > 0) {
            selectedLayers.reverse();
        }
        const tasks = []
        for (let i = 0; i < selectedLayers.length; i++) {
            tasks.push(clipSelectedLayerPromise(boundary, selectedLayers[i], false));
        }
        for (let j = 0; j < allLayerIds.length; j++) {
            if (!selectedLayers.includes(allLayerIds[j])) {
                tasks.push(clipSelectedLayerPromise(boundary, allLayerIds[j], false));
            }
        }

        Promise.all(tasks).then(function(results){
            loadingSpinner1.style.display = "none";
            ccaToolBtn.disabled = false;
            getDatasets(inputString);

            for (let i=0; i < inputs.length; i++) {
                addedLayers.push(inputs[i]);
            }

        });
    }

    ccaToolBtn.onclick = (e) => {
        e.preventDefault();
        window.location.href = selectedScenario.dataset.url + '&boundary=' + boundary + '&geoId=' + geoId;
    }
})()
