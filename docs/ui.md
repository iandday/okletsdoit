## Cotton Templates


### Object.Delete-Script
  Javascript to support an object's delete modal
### Object.Delete-Modal
  Delete modal, contents populated by AJAX call
### Object.Status
  Status badge for object
### Object.Menu
  Dropdown menu for actions related to an object
### Object-Detail.Detail-Actions
  Section of an object's detail card which provides buttons for the actions related to the object
#### Child Components

  * Buttons.View-Link
  * Buttons.View-Image
  
### Parent Detail
  Detail view for an object which contains associated child objects
#### Child Components

  * Object-Detail.Detail-Actions
  * Object.Delete-Script
  * Object.Delete-Modal
  * Object.Status
  * Buttons.Edit-Object
  * Buttons.Delete-Object
  * Buttons.Add-Object

  
#### Required Context

* block_title: (str) contents of `title` HTML tag
* breadcrumbs: (list({"title":str, "url": str|None})) Breadcrumb contents, title and url
* title: (str) The page's title
* object: (Model) Current model instance
* edit_url: (str) URL to edit the object's values
* status: (bool) Object's status
* status_text: (str) Status badge content
* link_url: (str) URL for the `view_link` component
* image_url: (str) URL for the `view_image` component
* delete_modal_url: (str) URL which provides the delete modal's context, the slug will be added by the JS
  
### Object Detail
  Detail view for an object
#### Child Components

  * Object-Detail.Detail-Actions
  * Object.Delete-Script
  * Object.Delete-Modal
  * Object.Add-Attachment-Modal 
  * Object.Status
  * Buttons.Edit-Object
  * Buttons.Delete-Object
  * Buttons.Add-Attachment

  
#### Required Context

* block_title: (str) contents of `title` HTML tag
* breadcrumbs: (list({"title":str, "url": str|None})) Breadcrumb contents, title and url
* title: (str) The page's title
* object: (Model) Current model instance
* edit_url: (str) URL to edit the object's values
* status: (bool) Object's status
* status_text: (str) Status badge content
* link_url: (str) URL for the `view_link` component
* image_url: (str) URL for the `view_image` component
* delete_modal_url: (str) URL which provides the delete modal's context, the slug will be added by the JS
* attach_submit_url
* attach_form: Form
* attachments: queryset from `Attachment.objects.attachments_for_object(obj).all()`

## Cotton Migration
* Core
  * Idea Detail
* Contacts
  * Contact Detail
* Deadline
  * Deadline Detail
  * List Detail
  * All Deadlines
* Expenses
  * Expense Detail
  * Category Detail
* Guestlist
* List
  * Entry Detail
  * List Detail
---

Attachments
* Expenses
* List Entry
* Contact
* Idea

Shared Helpers
* Object Delete Modal
  * Guestlist
    * All Guests
    * Guest Detail
    * Guest Group Detail
    * Guest Group Summary
  * Timeline
    * Timeline List
    * Timeline Detail
  * Inspiration
    * Inspiration Detail



* Complete Form
  * Guestlist
    * Guest Group
    * Guest
  * Core
      * Timeline
      * Inspiration
      * Idea
  * Contacts
      * File
      * Contact
  * Expense
    * Expense
    * Category
  * Deadline
    * Deadline
    * Deadline List
  * List
    * List
    * List Entry


* List Card Options
  * Deadline:Deadline Summary
  * Core: Idea List