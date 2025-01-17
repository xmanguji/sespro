class UtilService {
  static groupDataByMonth(dataList) {
    const groupedData = {};

    dataList.forEach((data) => {
      const date = new Date(data.date_submitted);
      const month = date.getMonth() + 1; // getMonth returns 0-11, so adding 1 to get 1-12
      const monthName = this.getMonthName(month)
      if (!groupedData[month]) {
        groupedData[monthName] = [];
      }

      groupedData[monthName].push(data);
    });

    return groupedData;
  }
  static getMonthName(monthNumber) {
    const months = [
      'Jan', 'Feb', 'Mar', 'Apr',
      'May', 'Jun', 'Jul', 'Aug',
      'Sep', 'Oct', 'Nov', 'Dec'
    ];

    return months[monthNumber - 1];
  }

  static getGraphColor(index) {
    switch (index) {
      case 0:
        return 'green';
      case 1:
        return 'yellow';
      case 2:
        return 'blue';
      case 3:
        return 'red';
      case 4:
        return 'indigo';
      default:
        return 'purple';
    }
  }

}

export default UtilService;
