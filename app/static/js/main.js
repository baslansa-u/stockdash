const tbody = document.getElementById('stock-body');

fetch('/api/stock')
  .then(res => res.json())
  .then(data => {
    tbody.innerHTML = '';

    for (const symbol in data) {
      const stock = data[symbol];
      const tradeTargets = {
        "ACHR": { entry: 10, exit: [13, 17, 21] },
        "INTC": { entry: 11, exit: [17, 21, 25] },
        "NVDA": { entry: 120, exit: [145, 170, 180] },
        "AEO": { entry: 10, exit: [13, 17, 21] },
        "ASTS": { entry: 60, exit: [65, 70, 80] },
      };

      const row = document.createElement('tr');

      if (stock.error) {
        row.innerHTML = `<td colspan="6" class="text-danger text-center">${symbol}: ${stock.error}</td>`;
      } else {
        const quote = stock.quote;
        const logo = stock.logo || '';
        const name = stock.name || symbol;
        const targetPrices = tradeTargets[symbol]?.exit?.join(' / ') || '-';

        const status = (symbol, currentPrice) => {
          const target = tradeTargets[symbol];
          if (!target) return "รอ";

          if (currentPrice <= target.entry) return "ควรซื้อ";
          const [exit1, exit2, exit3] = target.exit;
          if (currentPrice >= exit1) return "แนะนำให้ขาย";
          return "รอ";
        };

        row.innerHTML = `
        <td class="symbol-cell">
          <div>
            <img src="${logo}" alt="${name} Logo" class="rounded-circle">
            <strong>${symbol}</strong>
          </div>
        </td>
        <td class="align-middle">${name}</td>
        <td class="align-middle text-success text-center">$${quote.c.toFixed(2)}</td>
        <td class="align-middle text-center">< $${tradeTargets[symbol]?.entry ?? '-'}</td>
        <td class="align-middle text-center">${targetPrices}</td>
        <td class="align-middle text-center">${status(symbol, quote.c)}</td>
      `;
      }
      tbody.appendChild(row);
    }
  })
  .catch(error => {
    tbody.innerHTML = `<tr><td colspan="6" class="text-danger text-center">เกิดข้อผิดพลาดในการโหลดข้อมูล</td></tr>`;
    console.error(error);
  });
