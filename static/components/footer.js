export class HbnbFooter extends HTMLElement {
    constructor() {
      super();
    }

    // connect component
    connectedCallback() {
        // const shadow = this.attachShadow({ mode: "closed" });
        this.innerHTML = `
            <span>
                &copy; HBnB Foundation 2024
            </span>
        `;
    }
}
window.customElements.define('hbnb-footer', HbnbFooter);