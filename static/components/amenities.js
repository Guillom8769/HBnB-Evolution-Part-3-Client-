import { HbnbCheckbox } from "./checkbox.js"

export class HbnbAmenities extends HTMLElement {
    static self;

    constructor() {
      super();
    }

    // connect component
    connectedCallback() {
        // store a ref to the component
        HbnbAmenities.self = this;

        let amenCheckboxesHtml = HbnbAmenities.#createAmenitiesMenuCheckboxes();

        // Note that the submenu div is purposely placed before the button.
        // This is becuase the CSS I use to create the arrow animation
        // uses the 'sibling' selector and it will only work if the button is after the div.
        this.innerHTML = `
            <span id="amenities-counter" state="hide">
                <span class="amount">0</span>
                <span>selected</span>
            </span>
            <div id="amenities-submenu" state="hide">
                <div class="instruct">
                    Choose the ones that you want
                </div>
                <div class="items">`
                    + amenCheckboxesHtml +
                `</div>
                <div class="confirm">
                    <button id="btn-specific-amenities-ok" type="button">OK</button>
                </div>
            </div>
            <button id="btn-specific-amenities-select" type="button">
                <span>Please select</span>
                <span class="arrows">&raquo;</span>
            </button>
        `;

        HbnbAmenities.#init(this);
    }


    // --- Private + Public Methods ---

    static #createAmenitiesMenuCheckboxes() {
        let searchedAmen = [];

        // hbnb.searched.amen will either be an empty string (All) or an array of stuff (Specific)
        if (hbnb.searched && hbnb.searched.amen && Array.isArray(hbnb.searched.amen) && hbnb.searched.amen.length > 0) {
            searchedAmen = hbnb.searched.amen
        }

        // At this point, searchedAmen is either an empty array or an array containing the previous choices

        let amenGroupName = "amenities-specific-group[]";
        let amenCheckboxesHtml = ``;

        for (let amenityId in hbnb.amenities) {
            let isAmenChecked = ((searchedAmen.length > 0 && searchedAmen.includes(amenityId)) || searchedAmen.length == 0) ? "checked" : "";
            let amenityName = hbnb.amenities[amenityId];

            // If searchedAmen was empty, all checkboxes will be checked.
            // Otherwise, only a few specific amenities will be checked

            amenCheckboxesHtml += `<hbnb-checkbox name="` + amenGroupName + `" value="` + amenityId + `" label="` + amenityName + `" ` + isAmenChecked + ` ></hbnb-checkbox>`;
        }

        return amenCheckboxesHtml;
    }

    static setMenuVisibility(state) {
        HbnbAmenities.self.querySelector("#amenities-submenu").setAttribute("state", state);
    }

    static setCounterVisibility(state) {
        HbnbAmenities.self.querySelector("#amenities-counter").setAttribute("state", state);
    }

    static emitSelectionAndUpdateCounter(checkboxes) {
        let total = Object.keys(hbnb.amenities).length;
        let curr = 0;
        let selected = [];

        for (let c of checkboxes) {
            if (c.checked) {
                selected.push(c.value)
                curr++
            }
        }

        // Store the data in the the global object
        hbnb.form.request.amenities_checkboxes = selected;

        // I initially tried emitting the data back using a custom event but it didn't work lol.
        // The searchForm component does not exist at this point yet as it is created after Amenities
        // so there is nothing to catch the emitted event haha.

        // Update the html text of the counter
        HbnbAmenities.self.querySelector("#amenities-counter .amount").innerHTML = curr + '/' + total;
    }


    // --- Init ---

    static #init() {
        // Let's add a click event listener for the button in this component
        HbnbAmenities.self.querySelector("#btn-specific-amenities-select").addEventListener('click', function() {
            HbnbAmenities.setMenuVisibility("show");
            
            // Hmm... we have a small problem here...
            // I want to auto-select the 'specific' option when the user clicks the button.
            // How do we set the 'specific' radio to 'checked' from within this component?
            // We need some way of reaching out and doing something to the parent component.
            // Let's try emitting a custom event!
            let menuButtonClicked = new CustomEvent("amenities_menu_button_clicked", {
                bubbles: true,
                cancelable: false,
            });
            HbnbAmenities.self.dispatchEvent(menuButtonClicked);
        });

        // Add change event listeners to the checkboxes + update counter value
        let checkboxes = HbnbAmenities.self.querySelectorAll("#amenities-submenu input[type='checkbox']");
        for (let c of checkboxes) {
            c.addEventListener('click', function() {
                HbnbAmenities.emitSelectionAndUpdateCounter(checkboxes);
            })
        }
        HbnbAmenities.emitSelectionAndUpdateCounter(checkboxes);

        HbnbAmenities.self.querySelector("#btn-specific-amenities-ok").addEventListener('click', function() {
            HbnbAmenities.setMenuVisibility("hide");
        });
    }
}

window.customElements.define('hbnb-amenities', HbnbAmenities);