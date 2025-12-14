<script lang="ts">
    type iAccommodation = {
        name: string;
        description: string;
        url: string;
        phone: string;
        address: string;
        type: string;
    };

    const Accommodations: iAccommodation[] = [
        {
            name: "Holiday Inn Express Hocking Hills",
            description:
                "Located about 20 minutes from the venue, this hotel offers modern amenities and a complimentary breakfast.",
            url: "https://www.ihg.com/holidayinnexpress/hotels/us/en/logan/loaoh/hoteldetail?cm_mmc=GoogleMaps-_-EX-_-US-_-LOAOH",
            phone: "740-385-7700",
            address: "12916 Grey St, Logan, OH 43138",
            type: "hotel",
        },
        {
            name: "Hocking Hills State Park Lodge",
            description:
                "81 guestrooms full of rustic charm and modern comforts, located within Hocking Hills State Park.",
            url: "https://www.hockinghillsparklodge.com/lodging/guest-room",
            phone: "740-270-610",
            address: "20020 State Route 664 South, Logan, OH 43138",
            type: "hotel",
        },
        {
            name: "VRBO",
            description: "Find a cozy cabin or home rental in the Hocking Hills area.",
            url: "https://www.vrbo.com/search?destination=16187%20Kreashbaum%20Rd%2C%20Rockbridge%2C%20OH%2043149%2C%20USA&flexibility=1_DAY&searchRange=2026-06-01_2026-06-30&adults=2&sort=RECOMMENDED&upsellingNumNightsAdded=&theme=&userIntent=&semdtl=&upsellingDiscountTypeAdded=&categorySearch=",
            phone: "",
            address: "",
            type: "home",
        },
        {
            name: "Airbnb",
            description: "Find a cozy cabin or home rental in the Hocking Hills area.",
            url: "https://www.airbnb.com/s/16187-Kreashbaum-Road--Rockbridge--OH/homes?refinement_paths%5B%5D=%2Fhomes&place_id=ChIJDzcrPaHsR4gR1pkhZtsMNoY&adults=1",
            phone: "",
            address: "",
            type: "home",
        },
        {
            name: "Top O' The Caves Campground",
            description: "Offers camping sites and cabin rentals in the Hocking Hills area.",
            url: "https://www.campspot.com/park/top-o-the-caves-campground",
            phone: "740-385-6566",
            address: "26780 Chapel Ridge Rd, South Bloomingville, OH 43152",
            type: "camping",
        },
        {
            name: "Campbell Cove Campground by Lake Logan",
            description: "Offers full hook up RV sites, camping cabins and tent sites.",
            url: "https://www.campbellcovecampgrounds.com/",
            phone: "740-205-2024",
            address: "30713 Lake Logan Rd, Logan, OH 43138",
            type: "camping",
        },
    ];
</script>

<div class="mx-auto my-16 max-w-7xl px-4 sm:px-6 lg:px-8">
    <h2
        class="text-center text-2xl leading-tight font-bold sm:text-3xl md:text-4xl lg:text-4xl xl:text-5xl bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent mb-4">
        Need a Place to Stay?
    </h2>
    <p class="text-base-content/70 text-lg text-center mb-12 max-w-3xl mx-auto">
        We've compiled a list of nearby accommodations to make your stay comfortable. Whether you prefer a hotel, cabin
        rental, or camping under the stars, there's something for everyone!
    </p>

    <!-- Accommodations Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-7xl mx-auto px-4">
        {#each Accommodations as accommodation, index}
            <div
                class="card bg-base-200 shadow-xl border border-base-300 hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
                <div class="card-body">
                    <!-- Icon based on type -->
                    <div class="flex items-start justify-between mb-2">
                        {#if accommodation.type === "hotel"}
                            <div class="badge badge-accent badge-sm rounded-full p-4 m-3">
                                <span class="iconify lucide--hotel size-6 text-accent-content"></span>Hotel
                            </div>
                        {:else if accommodation.type === "home"}
                            <div class="badge badge-accent badge-sm rounded-full p-4 m-3">
                                <span class="iconify lucide--home size-6 text-accent-content"></span>Rental
                            </div>
                        {:else}
                            <div class="badge badge-accent badge-sm rounded-full p-4 m-3">
                                <span class="iconify lucide--tent size-6 text-accent-content"></span>Camping
                            </div>
                        {/if}
                    </div>

                    <h3 class="card-title text-primary-content text-lg mb-2">{accommodation.name}</h3>
                    <p class="text-primary-content text-sm mb-4 line-clamp-3">{accommodation.description}</p>

                    <!-- Contact Info -->
                    <div class="space-y-2 mb-4">
                        {#if accommodation.phone}
                            <div class="flex items-center gap-2 text-sm text-primary-content">
                                <span class="iconify lucide--phone size-4"></span>
                                <a href="tel:{accommodation.phone}" class="hover:text-primary transition-colors">
                                    {accommodation.phone}
                                </a>
                            </div>
                        {/if}
                        {#if accommodation.address}
                            <div class="flex items-start gap-2 text-sm text-primary-content">
                                <span class="iconify lucide--map-pin size-4 mt-0.5 flex-shrink-0"></span>
                                <span class="line-clamp-2">{accommodation.address}</span>
                            </div>
                        {/if}
                    </div>

                    <!-- Action Button -->
                    <div class="card-actions justify-end mt-auto">
                        <a
                            href={accommodation.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            class="btn btn-primary btn-sm gap-2">
                            <span>View Details</span>
                            <span class="iconify lucide--external-link size-4"></span>
                        </a>
                    </div>
                </div>
            </div>
        {/each}
    </div>
</div>
