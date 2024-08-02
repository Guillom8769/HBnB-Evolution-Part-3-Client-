export class HbnbAdminHeader extends HTMLElement {
    constructor() {
      super();
    }

    // connect component
    connectedCallback() {
        // const shadow = this.attachShadow({ mode: "closed" });
        this.innerHTML = `
            <div class="content">
                <div class="title">Admin Page</div>
            </div>
        `;
    }
}
window.customElements.define('hbnb-admin-header', HbnbAdminHeader);