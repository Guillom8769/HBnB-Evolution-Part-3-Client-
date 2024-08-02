export class HbnbRadio extends HTMLElement {
    constructor() {
      super();
    }

    // connect component
    connectedCallback() {
        let name = this.attributes.name.value
        let value = this.attributes.value.value
        let label = this.attributes.label.value
        let checked = this.attributes.checked ? "checked" : ""

        this.innerHTML = `
            <label>
                <input type="radio" name="` + name + `" value="` + value + `" ` + checked + ` />
                <span>` + label + `</span>
            </label>
        `;
    }
}

window.customElements.define('hbnb-radio', HbnbRadio);