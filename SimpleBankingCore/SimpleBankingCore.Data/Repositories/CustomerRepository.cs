#nullable enable
using Microsoft.EntityFrameworkCore;
using SimpleBankingCore.Data.Context;
using SimpleBankingCore.Core.Models;
using System.Threading.Tasks;

namespace SimpleBankingCore.Data.Repositories
{
    public class CustomerRepository : GenericRepository<Customer>
    {
        public CustomerRepository(BankingDbContext context) : base(context) { }

        public async Task<Customer?> GetByEmailAsync(string email)
        {
            return await _dbSet.FirstOrDefaultAsync(c => c.Email == email);
        }

        public async Task<Customer?> GetByIdWithAccountsAsync(int customerId)
        {
            return await _dbSet
                .Include(c => c.Accounts)
                .FirstOrDefaultAsync(c => c.CustomerId == customerId);
        }

        public async Task<Customer?> GetByEmailWithAccountsAsync(string email)
        {
            return await _dbSet
                .Include(c => c.Accounts)
                .FirstOrDefaultAsync(c => c.Email == email);
    }
}
}
