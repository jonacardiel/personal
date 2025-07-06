using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;
using SimpleBankingCore.Data.Context;

namespace SimpleBankingCore.Data
{
    public class BankingDbContextFactory : IDesignTimeDbContextFactory<BankingDbContext>
    {
        public BankingDbContext CreateDbContext(string[] args)
        {
            var optionsBuilder = new DbContextOptionsBuilder<BankingDbContext>();
            // SQLite connection string (creates a file in your project directory)
            optionsBuilder.UseSqlite("Data Source=SimpleBankingCore.db");

            return new BankingDbContext(optionsBuilder.Options);
        }
    }
}