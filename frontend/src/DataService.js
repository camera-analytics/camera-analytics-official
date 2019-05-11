class DataService {
  constructor() {
    this._BASE_URL = 'http://127.0.0.1:5000/api'
  }

  currentCustomerCounts() {
    return new Promise((success, fail) => {
      fetch(`${this._BASE_URL}/customers/count`).then(response => {
        response.json().then(success)
      })
    })
  }

  customerCounts() {
    return new Promise((success, fail) => {
      fetch(`${this._BASE_URL}/customers/counts`).then(response => {
        response.json().then(success)
      })
    })
  }

  customerPositions() {
    return new Promise((success, fail) => {
      fetch(`${this._BASE_URL}/positions`).then(response => {
        response.json().then(success)
      })
    })
  }
}

export default DataService
