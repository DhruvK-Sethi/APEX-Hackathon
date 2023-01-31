document.addEventListener("DOMContentLoaded", function() {
    let locLinkBuyer = document.getElementById("locationLinkBuyer")
    let locLinkSeller = document.getElementById("locationLinkSeller")
    let latFieldBuyer = document.getElementById("inputLatitudeBuyer")
    let latFieldSeller = document.getElementById("inputLatitudeSeller")
    let longFieldBuyer = document.getElementById("inputLongitudeBuyer")
    let longFieldSeller = document.getElementById("inputLongitudeSeller")

    locLinkBuyer.onclick = getLocation;
    locLinkSeller.onclick = getLocation;

    function getLocation() {
        if(navigator.geolocation){
            locLinkBuyer.innerHTML = "Please wait....."
            locLinkSeller.innerHTML = "Please wait....."
            navigator.geolocation.getCurrentPosition(fillPosition)
        }
    }

    function fillPosition(position) {
        latFieldBuyer.value = position.coords.latitude;
        latFieldSeller.value = position.coords.latitude;
        longFieldBuyer.value = position.coords.longitude;
        longFieldSeller.value = position.coords.longitude;
        locLinkBuyer.innerHTML = "Use my current location"
        locLinkSeller.innerHTML = "Use my current location"
    }

    fetch('/static/cities.json')
      .then(response => response.json())
      .then(data => {
        let cities = data;
        let states = [];
        let statesSelect = document.getElementById('states');
        let citiesSelect = document.getElementById('cities');

        for (let i = 0; i < cities.length; i++) {
          if (!states.includes(cities[i].state)) {
            states.push(cities[i].state);
          }
        }

        states.sort()
        for (let i = 0; i < states.length; i++) {
          let option = document.createElement('option');
          option.value = states[i];
          option.text = states[i];
          statesSelect.appendChild(option);
        }
        statesSelect.addEventListener('change', function() {
        citiesSelect.innerHTML = '<option value="" disabled selected>Select City</option>';
        let selectedState = this.value;
        let stateCities = [];

        for (let i = 0; i < cities.length; i++) {
            if (cities[i].state === selectedState) {
              stateCities.push(cities[i].name);
            }
        }

        stateCities.sort();

        for (let i = 0; i < stateCities.length; i++) {
            let option = document.createElement('option');
            option.value = stateCities[i];
            option.text = stateCities[i];
            citiesSelect.appendChild(option);
            }
        });
    });
});
