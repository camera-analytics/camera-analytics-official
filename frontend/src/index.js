import React from 'react'
import ReactDOM from 'react-dom'
import './index.css'
import App from './App'
import registerServiceWorker from './registerServiceWorker'

import insertCss from 'insert-css'
import css from 're-bulma/build/css'
try {
  if (typeof document !== 'undefined' || document !== null)
    insertCss(css, { prepend: true })
} catch (e) {}

ReactDOM.render(<App />, document.getElementById('root'))
registerServiceWorker()
