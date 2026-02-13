<!-- src/routes/planning/guest_list/[id]/edit/+page.svelte -->
<script lang="ts">
    import ProtectedPageHeader from "$lib/components/layouts/ProtectedPageHeader.svelte";
    import ProtectedPageShell from "$lib/components/layouts/ProtectedPageShell.svelte";
    import type { ActionData, PageData } from "./$types";

    const { data, form }: { data: PageData; form: ActionData } = $props();

    const relativeCrumbs = [
        { title: "Guest List", href: "/planning/guest_list" },
        { title: data.guestGroup.name, href: `/planning/guest_list/${data.guestGroup.id}` },
        { title: "Edit" },
    ];

    let isSubmitting = $state(false);
</script>

<ProtectedPageShell {relativeCrumbs}>
    <ProtectedPageHeader
        title="Edit Guest Group"
        description="Update the information for {data.guestGroup.name}"
        showButtons={false} />

    {#if form?.error}
        <div class="alert alert-error mb-6">
            <span class="icon-[lucide--alert-circle] size-6"></span>
            <span>{form.error}</span>
        </div>
    {/if}

    <form method="POST" class="max-w-4xl">
        <!-- Basic Information -->
        <div class="edit-card mb-6">
            <div class="edit-card-body">
                <h3 class="edit-card-title">Basic Information</h3>

                <label class="form-control">
                    <div class="label">
                        <span class="edit-card-field-name">Group Name <span class="text-error">*</span></span>
                    </div>
                    <input type="text" name="name" class="input input-bordered" value={data.guestGroup.name} required />
                    <div class="label">
                        <span class="edit-card-field-description">The name that identifies this guest group</span>
                    </div>
                </label>

                <label class="form-control">
                    <div class="label">
                        <span class="edit-card-field-name">Address Name</span>
                    </div>
                    <input
                        type="text"
                        name="address_name"
                        class="input input-bordered"
                        value={data.guestGroup.addressName || ""} />
                    <div class="label">
                        <span class="edit-card-field-description"
                            >Name to use for mailing addresses (e.g., "The Smith Family")</span>
                    </div>
                </label>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <label class="form-control">
                        <div class="label">
                            <span class="edit-card-field-name">Relationship</span>
                        </div>
                        <select name="relationship" class="select select-bordered">
                            <option value="Rel" selected={data.guestGroup.relationship === "Rel"}>Relative</option>
                            <option value="Fri" selected={data.guestGroup.relationship === "Fri"}>Friend</option>
                            <option value="Col" selected={data.guestGroup.relationship === "Col"}>Colleague</option>
                        </select>
                    </label>

                    <label class="form-control">
                        <div class="label">
                            <span class="edit-card-field-name">Priority</span>
                        </div>
                        <select name="priority" class="select select-bordered">
                            <option value="1" selected={data.guestGroup.priority === 1}>Low (1)</option>
                            <option value="2" selected={data.guestGroup.priority === 2}>Medium (2)</option>
                            <option value="3" selected={data.guestGroup.priority === 3}>High (3)</option>
                        </select>
                    </label>
                </div>
            </div>
        </div>

        <!-- Contact Information -->
        <div class="edit-card mb-6">
            <div class="edit-card-body">
                <h3 class="edit-card-title">Contact Information</h3>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <label class="form-control">
                        <div class="label">
                            <span class="edit-card-field-name">Email</span>
                        </div>
                        <input
                            type="email"
                            name="email"
                            class="input input-bordered"
                            value={data.guestGroup.email || ""} />
                    </label>

                    <label class="form-control">
                        <div class="label">
                            <span class="edit-card-field-name">Phone</span>
                        </div>
                        <input
                            type="tel"
                            name="phone"
                            class="input input-bordered"
                            value={data.guestGroup.phone || ""} />
                    </label>
                </div>
            </div>
        </div>

        <!-- Mailing Address -->
        <div class="edit-card mb-6">
            <div class="edit-card-body">
                <h3 class="edit-card-title">Mailing Address</h3>

                <label class="form-control">
                    <div class="label">
                        <span class="edit-card-field-name">Address Line 1</span>
                    </div>
                    <input
                        type="text"
                        name="address"
                        class="input input-bordered"
                        value={data.guestGroup.address || ""} />
                </label>

                <label class="form-control">
                    <div class="label">
                        <span class="edit-card-field-name">Address Line 2</span>
                    </div>
                    <input
                        type="text"
                        name="address_two"
                        class="input input-bordered"
                        value={data.guestGroup.addressTwo || ""} />
                </label>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <label class="form-control">
                        <div class="label">
                            <span class="edit-card-field-name">City</span>
                        </div>
                        <input
                            type="text"
                            name="city"
                            class="input input-bordered"
                            value={data.guestGroup.city || ""} />
                    </label>

                    <label class="form-control">
                        <div class="label">
                            <span class="edit-card-field-name">State</span>
                        </div>
                        <input
                            type="text"
                            name="state"
                            class="input input-bordered"
                            value={data.guestGroup.state || ""} />
                    </label>

                    <label class="form-control">
                        <div class="label">
                            <span class="edit-card-field-name">ZIP Code</span>
                        </div>
                        <input
                            type="text"
                            name="zip_code"
                            class="input input-bordered"
                            value={data.guestGroup.zipCode || ""} />
                    </label>
                </div>
            </div>
        </div>

        <!-- Additional Notes -->
        <div class="edit-card mb-6">
            <div class="edit-card-body">
                <h3 class="edit-card-title">Additional Notes</h3>

                <label class="form-control">
                    <div class="label">
                        <span class="edit-card-field-name">Notes</span>
                    </div>
                    <textarea name="notes" class="textarea textarea-bordered h-24"
                        >{data.guestGroup.notes || ""}</textarea>
                    <div class="label">
                        <span class="edit-card-field-description"
                            >Any additional information about this guest group</span>
                    </div>
                </label>
            </div>
        </div>

        <!-- Form Actions -->
        <div class="flex gap-4 justify-end">
            <a href="/planning/guest_list/{data.guestGroup.id}" class="btn btn-error">
                <span class="icon-[lucide--x] size-5"></span>
                Cancel
            </a>
            <button type="submit" class="btn btn-success" disabled={isSubmitting}>
                <span class="icon-[lucide--save] size-5"></span>
                {isSubmitting ? "Saving..." : "Save Changes"}
            </button>
        </div>
    </form>
</ProtectedPageShell>
