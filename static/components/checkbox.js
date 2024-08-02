export class HbnbCheckbox extends HTMLElement {
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
                <input type="checkbox" name="` + name + `" value="` + value + `" ` + checked + `>
                <span>` + label + `</span>
            </label>
        `;
    }
}

window.customElements.define('hbnb-checkbox', HbnbCheckbox);