using Microsoft.EntityFrameworkCore;
using SimpleBankingCore.Core.Models;
using System;

namespace SimpleBankingCore.Data.Context
{
    public class BankingDbContext : DbContext
    {
        public DbSet<Customer> Customers { get; set; }
        public DbSet<Account> Accounts { get; set; }
        public DbSet<Transaction> Transactions { get; set; }

        public BankingDbContext(DbContextOptions<BankingDbContext> options) : base(options) { }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // --- Customer Configurations ---
            modelBuilder.Entity<Customer>()
                .HasKey(c => c.CustomerId);

            modelBuilder.Entity<Customer>()
                .HasIndex(c => c.Email)
                .IsUnique();

            modelBuilder.Entity<Customer>()
                .HasMany(c => c.Accounts)
                .WithOne(a => a.Customer)
                .HasForeignKey(a => a.CustomerId)
                .OnDelete(DeleteBehavior.Cascade);

            // --- Account Configurations ---
            modelBuilder.Entity<Account>()
                .HasKey(a => a.AccountId);

            modelBuilder.Entity<Account>()
                .Property(a => a.CurrentBalance)
                .HasColumnType("decimal(18, 2)");

            modelBuilder.Entity<Account>()
                .HasMany(a => a.Transactions)
                .WithOne(t => t.Account)
                .HasForeignKey(t => t.AccountId)
                .OnDelete(DeleteBehavior.Cascade);

            // --- Transaction Configurations ---
            modelBuilder.Entity<Transaction>()
                .HasKey(t => t.TransactionId);

            modelBuilder.Entity<Transaction>()
                .Property(t => t.Amount)
                .HasColumnType("decimal(18, 2)");

            modelBuilder.Entity<Transaction>()
                .Property(t => t.BalanceAfterTransaction)
                .HasColumnType("decimal(18, 2)");

            // Optional: Seed initial data for testing
            // modelBuilder.Entity<Customer>().HasData(
            //     new Customer { CustomerId = 1, FirstName = "Alice", LastName = "Smith", Email = "alice@example.com", DateCreated = DateTime.UtcNow }
            // );
            // modelBuilder.Entity<Account>().HasData(
            //     new Account { AccountId = 101, CustomerId = 1, AccountType = SimpleBankingCore.Core.Enums.AccountType.Checking, CurrentBalance = 1000.00m, DateOpened = DateTime.UtcNow, IsActive = true }
            // );
        }
    }
}
