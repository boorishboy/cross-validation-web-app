function getCVLabels(array) {
  var xlables = [];
  for (let i = 1; i - 1 < array.length; i++) {
    xlables.push(i.toString())
  }
  return xlables;
}

function populateArray(array, data) {
  const populatedArray = [];
  for (let i = 0; i < array.length; i++) {
    populatedArray.push(data)
  }
  return populatedArray;
}


function plotRKF(dataRKF, data) {
  var trace1 = {
    x: getCVLabels(dataRKF),
    y: dataRKF,
    name: 'RKF Scores',
    error_y: {
      type: 'data',
      array: populateArray(dataRKF, data.results.cv_stddev),
      visible: true
    },
    type: 'bar'
  };
  var trace2 = {
    x: getCVLabels(dataRKF),
    y: populateArray(dataRKF, data.results.cv_mean),
    name: 'Mean',
    type: 'line'
  };
  var data_rkf = [trace1, trace2];
  var layout = {
    title: 'RepeatedKFold Scores',
    titlefont: {
      family: 'Roboto',
      size: 18,
    },
    xaxis: {
      'type': 'category',
      title: 'Number of Fold',
      titlefont: {
        family: 'Roboto',
        size: 18,
        color: 'lightgrey'
      }
    },
    autosize: true,
  };
  var config = {
    locale: 'pl',
    responsive: true,
    toImageButtonOptions: {
      filename: 'RKF_Scores_run_id_' + data.runid + "_" + data.upload_timestamp,
      format: 'png'
    }
  };



  Plotly.newPlot('data-val-rkf-plot', data_rkf, layout, config);
}

function plotCV(dataCV, data) {
  var trace1 = {
    x: getCVLabels(dataCV),
    y: dataCV,
    name: 'Cross Validation Scores',
    error_y: {
      type: 'data',
      array: populateArray(dataCV, data.results.cv_stddev),
      visible: true
    },
    type: 'bar'
  };
  var trace2 = {
    x: getCVLabels(dataCV),
    y: populateArray(dataCV, data.results.cv_mean),
    name: 'Mean',
    type: 'line'
  };
  var data_cv = [trace1, trace2];
  var layout = {
    title: 'Cross Validation Scores',
    titlefont: {
      family: 'Roboto',
      size: 18,
    },
    xaxis: {
      'type': 'category',
      title: 'Number of Fold',
      titlefont: {
        family: 'Roboto',
        size: 18,
        color: 'lightgrey'
      }
    },
    autosize: true,
  };
  var config = {
    locale: 'pl',
    responsive: true,
    toImageButtonOptions: {
      filename: 'CV_Scores_run_id_' + data.runid + "_" + data.upload_timestamp,
      format: 'png'
    }
  };



  Plotly.newPlot('data-val-cv-plot', data_cv, layout, config);
}

function plotOLS_first(y_data, percentage_error_vect_ols, data) {
  var trace1 = {
    x: y_data.slice(0, 75),
    y: percentage_error_vect_ols.slice(0, 75).map(function(x) {
      return x * 100.0
    }),
    name: 'percentage error BEEBS',
    mode: 'markers',
    type: 'scatter'
  };
  var trace2 = {
    x: y_data.slice(75),
    y: percentage_error_vect_ols.slice(75).map(function(x) {
      return x * 100.0
    }),
    name: 'percentage error IRIDA',
    mode: 'markers',
    type: 'scatter'
  };
  var trace3 = {
    x: y_data,
    y: populateArray(y_data, data.results.mean_percentage_error_ols),
    name: 'Mean',
    type: 'line'
  };
  var trace4 = {
    x: y_data,
    y: populateArray(y_data, data.results.median_percentage_error_ols),
    name: 'Median',
    type: 'line'
  };
  var trace5 = {
    x: y_data,
    y: populateArray(y_data, data.results.mean_abs_percentage_error_ols),
    name: '+MAPE',
    type: 'line'
  };
  var trace6 = {
    x: y_data,
    y: populateArray(y_data, -data.results.mean_abs_percentage_error_ols),
    name: '-MAPE',
    type: 'line'
  };
  var trace7 = {
    x: y_data,
    y: populateArray(y_data, (data.results.mean_percentage_error_ols + data.results.stddev_relative_error_ols)),
    name: 'mean relative error + SD',
    type: 'line'
  };
  var trace8 = {
    x: y_data,
    y: populateArray(y_data, (data.results.mean_percentage_error_ols - data.results.stddev_relative_error_ols)),
    name: 'mean relative error - SD',
    type: 'line'
  };
  var data_ols = [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8];
  var layout = {
    title: data.targetColumn + " using OLS",
    titlefont: {
      family: 'Roboto',
      size: 18,
    },
    xaxis: {
      type: 'log',
      title: 'True values [J]',
      titlefont: {
        family: 'Roboto',
        size: 18,
        color: 'lightgrey'
      }
    },
    yaxis: {
      title: "Relative error [%]",
      titlefont: {
        family: 'Roboto',
        size: 18,
        color: 'lightgrey'
      }
    },
    autosize: true,
  };
  var config = {
    locale: 'pl',
    responsive: true,
    toImageButtonOptions: {
      filename: 'OLS_error_run_id_' + data.runid + '_' + data.upload_timestamp,
      format: 'png'
    }
  };


  Plotly.newPlot('ols-error-plot', data_ols, layout, config);
};

function plotOLSCoefs(coefs, data) {
  var trace1 = {
    x: data.paramList.split(', '),
    y: coefs,
    name: 'Coefficients OLS',
    type: 'bar',
  };
  var data_coef_ols = [trace1];
  var layout = {
      title: 'OLS coefficients',
      titlefont: {
        family: 'Roboto',
        size: 18,
      },
    autosize: true,
};
var config = {
  locale: 'pl',
  responsive: true,
  toImageButtonOptions: {
    filename: 'OLS_coefs' + "id" + data.runid + "_" + data.upload_timestamp,
    format: 'png'
  }
};



Plotly.newPlot('ols-coef', data_coef_ols, layout, config);
}

function plotNNLS_eror(y_data, percentage_error_vect_nnls, data) {
  var trace1 = {
    x: y_data.slice(0, 75),
    y: percentage_error_vect_nnls.slice(0, 75).map(function(x) {
      return x * 100.0
    }),
    name: 'percentage error BEEBS',
    mode: 'markers',
    type: 'scatter'
  };
  var trace2 = {
    x: y_data.slice(75),
    y: percentage_error_vect_nnls.slice(75).map(function(x) {
      return x * 100.0
    }),
    name: 'percentage error IRIDA',
    mode: 'markers',
    type: 'scatter'
  };
  var trace3 = {
    x: y_data,
    y: populateArray(y_data, data.results.mean_percentage_error_nnls),
    name: 'Mean',
    type: 'line'
  };
  var trace4 = {
    x: y_data,
    y: populateArray(y_data, data.results.median_percentage_error_nnls),
    name: 'Median',
    type: 'line'
  };
  var trace5 = {
    x: y_data,
    y: populateArray(y_data, data.results.mean_abs_percentage_error_nnls),
    name: '+MAPE',
    type: 'line'
  };
  var trace6 = {
    x: y_data,
    y: populateArray(y_data, -data.results.mean_abs_percentage_error_nnls),
    name: '-MAPE',
    type: 'line'
  };
  var trace7 = {
    x: y_data,
    y: populateArray(y_data, (data.results.mean_percentage_error_nnls + data.results.stddev_relative_error_nnls)),
    name: 'mean relative error + SD',
    type: 'line'
  };
  var trace8 = {
    x: y_data,
    y: populateArray(y_data, (data.results.mean_percentage_error_nnls - data.results.stddev_relative_error_nnls)),
    name: 'mean relative error - SD',
    type: 'line'
  };
  var data_nnls = [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8];
  var layout = {
    title: data.targetColumn + " using NNLS",
    titlefont: {
      family: 'Roboto',
      size: 18,
    },
    xaxis: {
      type: 'log',
      title: 'True values [J]',
      titlefont: {
        family: 'Roboto',
        size: 18,
        color: 'lightgrey'
      }
    },
    yaxis: {
      title: "Relative error [%]",
      titlefont: {
        family: 'Roboto',
        size: 18,
        color: 'lightgrey'
      }
    },
    autosize: true,
  };
  var config = {
    locale: 'pl',
    responsive: true,
    toImageButtonOptions: {
      filename: 'NNLS_error_run_id' + data.runid + "_" + data.upload_timestamp,
      format: 'png'
    }
  };


  Plotly.newPlot('nnls-error-plot', data_nnls, layout, config);
};

function plotNNLSCoefs(coefs, data) {
  var trace1 = {
    x: data.paramList.split(', '),
    y: coefs,
    name: 'Coefficients NNLS',
    type: 'bar',
  };
  var data_coef_nnls = [trace1];
  var layout = {
      title: 'NNLS Coefficients',
      titlefont: {
        family: 'Roboto',
        size: 18,
      },
    autosize: true,

};
var config = {
  locale: 'pl',
  responsive: true,
  toImageButtonOptions: {
    filename: "NNLS_coefficients_run_id" + data.runid + "_" + data.upload_timestamp,
    format: 'png'
  }
};



Plotly.newPlot('nnls-coef', data_coef_nnls, layout, config);
}
