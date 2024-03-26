const tickerForm = document.getElementById("ticker-form");
const spinner = document.getElementById("spinner");
const tickerSymbol = document.querySelector("#id_ticker_symbol");
const alertContainer = document.getElementById("alert");
const alertCloseBtn = document.getElementById("alert-close-btn");
const pricesContainer = document.getElementById('prices-container');
let chart;

alertCloseBtn.addEventListener("click", () => {
  alertContainer.classList.add("hidden");
  alertContainer.classList.remove("flex");
});

tickerForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const regex = /^[a-zA-Z\.:\-]{3,20}$/;

  if (!tickerSymbol.value.match(regex)) {
    makeAlert('Please Enter a valid symbol like: "aapl", "amzn"');
    return;
  }

  spinner.classList.remove("hidden");

  const formData = new FormData();

  tickerForm.querySelectorAll("*[id]").forEach((element) => {
    let key = element.id.replace("id_", "");
    let value = element.value;
    formData.append(key, value);
  });

  let csrfToken = document.querySelector('input[type="hidden"]');
  formData.append("csrfmiddlewaretoken", csrfToken.value);

  fetchData(formData);
});

async function fetchData(formdata) {
  const response = await fetch("/", {
    method: "POST",
    body: formdata,
  });
  if (response.status === 200) {
    spinner.classList.add("hidden");
  }
  if (response.status !== 200) {
    spinner.classList.add("hidden");
    let error = await response.json();
    error = JSON.parse(error) ? JSON.parse(error).start_date[0].message : "Error";
    let message = error + "\nBad Request, Please make sure from you data";
    makeAlert(message);
    tickerSymbol.focus();
    return;
  }

  const data = await response.json();

  let dates = [];
  let openPrices = [];
  let closePrices = [];

  pricesContainer.innerHTML = '';

  data.forEach((row) => {
    let { Date: date, Open: open, Close: close } = row;
    dates.push(date);
    openPrices.push(open);
    closePrices.push(close);
    let rowDiv = createPricesRow(row);
    pricesContainer.appendChild(rowDiv);
  });

  makeChart(dates, openPrices, closePrices)

}

function makeAlert(message) {
  const p = alertContainer.querySelector("p");
  const text = document.createTextNode(message);
  p.innerHTML = "";
  p.appendChild(text);
  alertContainer.classList.remove("hidden");
  alertContainer.classList.add("flex");
}

function makeChart(yLabels, openPrices, closePrices) {

  const ctx = document.getElementById("myChart");

  let configurations = {
    type: "bar",
    data: {
      labels: yLabels,
      datasets: [
        {
          label: 'Open',
          data: openPrices,
          borderWidth: 1,
          backgroundColor: "#22c55e",
        },
        {
          label: "Close",
          data: closePrices,
          borderWidth: 1,
          backgroundColor: "#c70e0e",
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: false,
        },
      },
    },
  };

  if (chart) {
    chart.destroy()
    chart = new Chart(ctx, configurations);
  } else {
    chart = new Chart(ctx, configurations);
  }
}

function createPricesRow(row) {
  const mainDiv = document.createElement('div');
  mainDiv.setAttribute('class', 'flex items-center hover:bg-slate-200 px-2');
  
  const dateSpan = document.createElement('span');
  dateSpan.setAttribute('class', 'text-xs text-slate-500');
  dateSpan.innerHTML = row.Date;
  mainDiv.appendChild(dateSpan);

  const pricesDiv = document.createElement('div');
  pricesDiv.setAttribute('class', 'ml-auto flex items-center font-bold tracking-tighter gap-2');

  const openSpan = document.createElement('span');
  let openSpanText = document.createTextNode(row.Open.toFixed(2))
  openSpan.setAttribute('class', 'text-green-600');
  openSpan.setAttribute('title', 'open');
  openSpan.appendChild(openSpanText);
  pricesDiv.appendChild(openSpan);

  const closeSpan = document.createElement('span');
  let closeSpanText = document.createTextNode(row.Close.toFixed(2))
  closeSpan.setAttribute('class', 'text-red-600');
  closeSpan.setAttribute('title', 'close');
  closeSpan.appendChild(closeSpanText);
  pricesDiv.appendChild(closeSpan);

  mainDiv.appendChild(pricesDiv);

  return mainDiv;
}