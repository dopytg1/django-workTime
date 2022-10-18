on_time_line = document.getElementById("on_time_line")
late_line = document.getElementById("late_line")
on_time = parseInt(document.getElementById("on_time").textContent)
late = parseInt(document.getElementById("late").textContent)

// console.log(on_time, late)
function formatAsPercent(num) {
    return new Intl.NumberFormat('default', {
      style: 'percent',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(num / 100);
  }


function SetLinesWidth() {
    total = on_time + late
    on_time_width = (on_time/total) * 100
    late_width = (late/total) * 100
    
    
    on_time_line.style.width = formatAsPercent(on_time_width)
    late_line.style.width = formatAsPercent(late_width)
}

SetLinesWidth()
