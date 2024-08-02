export class HbnbHeader extends HTMLElement {
    constructor() {
      super();
    }

    // connect component
    connectedCallback() {
        // const shadow = this.attachShadow({ mode: "closed" });
        this.innerHTML = `
            <div class="content">
                <div class="title">Welcome to the HBnB Listings site!</div>
                <div class="subtitle">Find your perfect vacation getaway!</div>
            </div>
            <div class="status">
                <a href="/admin">Admin area</a>
            </div>
        `;
    }
}
window.customElements.define('hbnb-header', HbnbHeader);