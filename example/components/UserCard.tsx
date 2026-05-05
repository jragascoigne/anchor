// UserCard.tsx
// Example component showing Anchor's @Expects annotations.
// Run `anchor check` to validate these against your API.

// @Expects('email')
const email: string = "";

// @Expects('address.city')
const city: string = "";

// @Expects('address.geo.lat')
const lat: string = "";

// @Expects('company.name')
const companyName: string = "";

// Intentionally wrong — to show Anchor catching drift:

// @Expects('firstName')
const firstname: string = "";

// @Expects('profile.username')
const username: string = "";

// @Expects('phoneNumber')
const phone: string = "";
