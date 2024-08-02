export class HbnbSearchResults extends HTMLElement {
    static self;

    constructor() {
      super();
    }

    // connect component
    connectedCallback() {
        // store a ref to the component
        HbnbSearchResults.self = this;

        this.innerHTML = `
            <div class="none">
                <h1>Please run the Search above to find available properties!</h1>
            </div>
        `;
    }

    static renderResults() {
        let results = hbnb.form.response;
        let listings = `<ul class="listings">`;

        for (let countryName in results) {
            listings += `
                <li class="country_group">
                    <div class="country_name">` + countryName + `</div>
                    <ul class="cities">`;

            for (let cityName in results[countryName]) {
                listings += `
                        <li class="city_group">
                            <div class="city_name">` + cityName + `</div>
                            <ul>`;

                for (let placeIndex in results[countryName][cityName]) {
                    listings += HbnbSearchResults.#makePlaceHtml(results[countryName][cityName][placeIndex]);
                }

                listings += `
                            </ul>
                        </li>`;
            }

            listings += `
                    </ul>
                </li>
            `;
        }

        listings += `</ul>`;

        HbnbSearchResults.self.innerHTML = listings;
    }

    static #makePlaceHtml(place) {
        let placeHtml = ``;
        let placeAmenitiesHtml = `No amenities!`;

        if (place.amenities.length > 0) {
            placeAmenitiesHtml = ``;
            for (let amenityName of place.amenities) {
                placeAmenitiesHtml += `<span>` + amenityName + `</span>`;
            }
        }

        placeHtml = `
            <li class="place">
                <div class="name">` + place.name + `</div>
                <div class="details">
                    <div class="price">
                        <div class="digits">$` + place.price_per_night + `</div>
                        <div class="pax">per pax per night</div>
                    </div>
                    <div class="description">` + place.description + `</div>
                    <div class="address" latitude="` + place.latitude + `" longitude="` + place.longitude + `">
                        <span class="text">` + place.address + `</span>
                    </div>
                    <div class="amenities">
                        ` + placeAmenitiesHtml + `
                    </div>
                    <div class="accommodations">
                        <span class="rooms"><i class="fa-solid fa-house"></i>` + place.number_of_rooms + `</span>
                        <span class="bathrooms"><i class="fa-solid fa-bath"></i>` + place.number_of_bathrooms + `</span>
                        <span class="guests"><i class="fa-solid fa-person"></i>` + place.max_guests + `</span>
                    </div>
                </div>
            </li>
        `;

        return placeHtml;
    }
}

window.customElements.define('hbnb-search-results', HbnbSearchResults);