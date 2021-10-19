/* Copyright The IETF Trust 2021, All Rights Reserved
 *
 * JS support for the SessionDetailsForm
 * */
(function() {
  'use strict';

  /* Find the id prefix for each widget. Individual elements have a _<number> suffix. */
  function get_widget_ids(elements) {
    const ids = new Set();
    for (let ii=0; ii < elements.length; ii++) {
      const parts = elements[ii].id.split('_');
      parts.pop();
      ids.add(parts.join('_'));
    }
    return ids;
  }

  /* Set the 'type' element to a type valid for the currently selected purpose, if possible */
  function set_valid_type(type_elt, purpose, allowed_types) {
    const valid_types = allowed_types[purpose] || [];
    if (valid_types.indexOf(type_elt.value) === -1) {
      type_elt.value = (valid_types.length > 0) ? valid_types[0] : '';
    }
  }

  /* Hide any type options not allowed for the selected purpose */
  function update_type_option_visibility(type_option_elts, purpose, allowed_types) {
    const valid_types = allowed_types[purpose] || [];
    for (const elt of type_option_elts) {
      if (valid_types.indexOf(elt.value) === -1) {
        elt.setAttribute('hidden', 'hidden');
      } else {
        elt.removeAttribute('hidden');
      }
    }
  }

  /* Update visibility of 'type' select so it is only shown when multiple options are available */
  function update_widget_visibility(elt, purpose, allowed_types) {
    const valid_types = allowed_types[purpose] || [];
    if (valid_types.length > 1) {
      elt.removeAttribute('hidden'); // make visible
    } else {
      elt.setAttribute('hidden', 'hidden'); // make invisible
    }
  }

  /* Update the 'type' select to reflect a change in the selected purpose */
  function update_type_element(type_elt, purpose, type_options, allowed_types) {
    update_widget_visibility(type_elt, purpose, allowed_types);
    update_type_option_visibility(type_options, purpose, allowed_types);
    set_valid_type(type_elt, purpose, allowed_types);
  }

  function update_name_field_visibility(name_elt, purpose) {
    const row = name_elt.closest('tr');
    if (purpose === 'regular') {
      row.setAttribute('hidden', 'hidden');
    } else {
      row.removeAttribute('hidden');
    }
  }

  /* Factory for event handler with a closure */
  function purpose_change_handler(name_elt, type_elt, type_options, allowed_types) {
    return function(event) {
      const purpose = event.target.value;
      update_name_field_visibility(name_elt, purpose);
      update_type_element(type_elt, purpose, type_options, allowed_types);
    };
  }

  function add_purpose_change_handler(form) {
    const id_prefix = 'id_' + form.dataset.prefix;
    const name_elt = document.getElementById(id_prefix + '-name');
    const purpose_elt = document.getElementById(id_prefix + '-purpose');
    const type_elt = document.getElementById(id_prefix + '-type');
    const type_options = type_elt.getElementsByTagName('option');
    const allowed_types = JSON.parse(type_elt.dataset.allowedOptions);

    // update on future changes
    purpose_elt.addEventListener(
      'change',
      purpose_change_handler(name_elt, type_elt, type_options, allowed_types)
    );

    // update immediately
    update_type_element(type_elt, purpose_elt.value, type_options, allowed_types);
    update_name_field_visibility(name_elt, purpose_elt.value);

    // hide the purpose selector if only one option
    const purpose_options = purpose_elt.querySelectorAll('option:not([value=""])');
    if (purpose_options.length < 2) {
      purpose_elt.closest('tr').setAttribute('hidden', 'hidden');
    }
  }

  /* Initialization */
  function on_load() {
    /* Find elements that are parts of the session details forms. This is an
    * HTMLCollection that will update if the DOM changes, so ok to evaluate immediately. */
    const forms = document.getElementsByClassName('session-details-form');
    for (const form of forms) {
      add_purpose_change_handler(form);
    }
  }
  window.addEventListener('load', on_load, false);
})();