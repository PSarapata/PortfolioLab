document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });


  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;
      document.getElementById('form-donate').scrollIntoView();
      // TODO: get data from inputs and show them in summary
    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
  submit(e) {
    e.preventDefault();
    this.currentStep++;
    this.updateForm()
  };
}

  function hideThemInputs(event) {

    event.preventDefault();

    /*
    * This function is bound to donation form's submit (next) button. Ajax request is sent to an endpoint,
    * it then checks for orgs with chosen categories and hides the remainder.
    */

    this.$checkedCategories = document.querySelector("div[data-step='1']").querySelectorAll('input:checked');
    /**
     * Since we now have selected the input nodes with category IDs, we could compare those with the queryset of related organizations
     */

    let categories = [];

    this.$checkedCategories.forEach(cat => {
      categories.push(cat.value);
    });

    /**
     * We are passing data with POST to a custom Back End endpoint, which allows us to get filtered DB results, which we can then use to hide
     * stuff dynamically.
     */
    $.ajax({
      type: 'POST',
      url: "http://localhost:8000/app/ajax/selected-institutions/",
      data: JSON.stringify({"serializedData": categories}),
      success: (response) => {
        console.log(response)

        // Get ID list from the response:
        let resp = JSON.parse(response)
        let idList = Array.from(resp.idList);
        let availableOrgs = document.querySelector('div[data-step="3"]').querySelectorAll('input');

        // Check if the organisation has the chosen categories:
        // No? --> hide it

        availableOrgs.forEach(org => {
          if (!idList.includes(parseInt(org.value))) {
            org.parentElement.parentElement.style.display = 'none';
          }
        });
      },
      error: (response) => {
        alert(response["responseJSON"]["error"]);
      }
    });
  }

  // STEP 5 data render
  function displaySummary(event) {

    event.preventDefault();

    const selectedCategories = document.querySelector("div[data-step='1']").querySelectorAll('input:checked')
    categoryNames = []
    selectedCategories.forEach(cat => {
        const catName = cat.parentElement.querySelector('span.description').innerText
        categoryNames.push(catName)
    })

    const qty = document.querySelector('div[data-step="2"]').querySelector('input').value
    const pasteQtyAndNamesHere = document.getElementById('summ-donation')
    pasteQtyAndNamesHere.innerText = `${qty} worki ${categoryNames}`

    const address = document.querySelector('input[name="address"]').value
    const city = document.querySelector('input[name="city"]').value
    const postcode = document.querySelector('input[name="postcode"]').value
    const phone = document.querySelector('input[name="phone"]').value
    const address_data = [address, city, postcode, phone]
    const claimAddress = document.getElementById('claim-address')

    address_data.forEach(el => {
      const li = document.createElement('li')
      li.innerText = el
      claimAddress.appendChild(li)
    })

    const date = document.querySelector('input[name="data"]').value
    const time = document.querySelector('input[name="time"]').value
    const more_info = document.querySelector('textarea[name="more_info"]').value
    const time_data = [date, time, more_info]
    const claimDate = document.getElementById('claim-date')

    time_data.forEach(el => {
      const li = document.createElement('li')
      li.innerText = el
      claimDate.appendChild(li)
    })

    const orgs = document.querySelector('div[data-step="3"').querySelectorAll('input:checked')

    orgs.forEach(org => {
        const chosen_org = org.parentElement.querySelector('span.description > div.title').innerText
        const pasteOrgHere = document.getElementById('summ-org')
        pasteOrgHere.innerText = `Dla ${chosen_org} w ${city}`
    })
  }

  const targetButton = document.querySelector('div[data-step="1"]').querySelector('button')
  targetButton.addEventListener("click", hideThemInputs, once=true)

  const showSummaryButton = document.querySelector('div[data-step="4"]').querySelector('button.next-step')
  showSummaryButton.addEventListener('click', displaySummary)

  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});
